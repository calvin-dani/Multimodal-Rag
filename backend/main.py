from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import torch
from transformers import CLIPProcessor, CLIPModel, Speech2TextProcessor, Speech2TextForConditionalGeneration
import numpy as np
import io
import wave
from PIL import Image
import base64
from pydantic import BaseModel
from typing import List, Dict, Any
import os
import json
from pydub import AudioSegment
import tempfile

app = FastAPI(title="Multimodal RAG API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for models
clip_model = None
clip_processor = None
speech_model = None
speech_processor = None

# In-memory storage for documents and embeddings
documents = []
embeddings = []

class QueryRequest(BaseModel):
    query: str

class DocumentResponse(BaseModel):
    id: str
    content: str
    modality: str
    similarity_score: float

class RAGResponse(BaseModel):
    answer: str
    relevant_documents: List[DocumentResponse]

def load_models():
    """Load CLIP and Speech-to-Text models"""
    global clip_model, clip_processor, speech_model, speech_processor
    
    print("Loading CLIP model...")
    clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    
    print("Loading Speech-to-Text model...")
    speech_model = Speech2TextForConditionalGeneration.from_pretrained("facebook/s2t-medium-librispeech-asr")
    speech_processor = Speech2TextProcessor.from_pretrained("facebook/s2t-medium-librispeech-asr")
    
    print("Models loaded successfully!")

def process_audio(audio_file) -> str:
    """Convert audio to text using speech-to-text model"""
    try:
        # Read audio file
        audio_data = audio_file.read()
        audio_file.seek(0)  # Reset file pointer
        
        # Convert to AudioSegment
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_data))
        
        # Downsample to 16000 Hz
        sampling_rate = 16000
        audio_segment = audio_segment.set_frame_rate(sampling_rate)
        
        # Convert to numpy array
        audio_waveform = np.array(audio_segment.get_array_of_samples(), dtype=np.float32)
        
        # Process with speech-to-text model
        inputs = speech_processor(audio_waveform, sampling_rate=sampling_rate, return_tensors="pt")
        generated_ids = speech_model.generate(inputs["input_features"], attention_mask=inputs["attention_mask"])
        
        # Decode to text
        transcription = speech_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return transcription
    except Exception as e:
        print(f"Error processing audio: {e}")
        return "Error transcribing audio"

def get_embeddings(texts: List[str], images: List[Image.Image] = None) -> torch.Tensor:
    """Get embeddings for texts and images using CLIP"""
    text_embeddings = None
    image_embeddings = None
    
    if texts:
        inputs = clip_processor(text=texts, return_tensors="pt", padding=True)
        text_embeddings = clip_model.get_text_features(**inputs)
    
    if images:
        inputs = clip_processor(images=images, return_tensors="pt")
        image_embeddings = clip_model.get_image_features(**inputs)
    
    return text_embeddings, image_embeddings

def calculate_similarity(query_embedding: torch.Tensor, doc_embeddings: torch.Tensor) -> List[float]:
    """Calculate cosine similarity between query and document embeddings"""
    from torch.nn.functional import cosine_similarity
    
    similarities = []
    for i in range(doc_embeddings.shape[0]):
        sim = cosine_similarity(
            query_embedding.unsqueeze(0), 
            doc_embeddings[i].unsqueeze(0)
        ).item()
        similarities.append(sim)
    
    return similarities

@app.on_event("startup")
async def startup_event():
    load_models()

@app.get("/")
async def root():
    return {"message": "Multimodal RAG API is running!"}

@app.post("/upload/text")
async def upload_text(file: UploadFile = File(...)):
    """Upload and process text document"""
    try:
        content = await file.read()
        text_content = content.decode('utf-8')
        
        # Get embedding
        text_embeddings, _ = get_embeddings([text_content])
        
        # Store document
        doc_id = f"text_{len(documents)}"
        documents.append({
            "id": doc_id,
            "content": text_content,
            "modality": "text",
            "filename": file.filename
        })
        embeddings.append(text_embeddings[0])
        
        return {"message": "Text document uploaded successfully", "doc_id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    """Upload and process image document"""
    try:
        content = await file.read()
        image = Image.open(io.BytesIO(content))
        
        # Get embedding
        _, image_embeddings = get_embeddings(texts=[], images=[image])
        
        # Store document
        doc_id = f"image_{len(documents)}"
        documents.append({
            "id": doc_id,
            "content": f"Image: {file.filename}",
            "modality": "image",
            "filename": file.filename,
            "image_data": base64.b64encode(content).decode()
        })
        embeddings.append(image_embeddings[0])
        
        return {"message": "Image document uploaded successfully", "doc_id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload/audio")
async def upload_audio(file: UploadFile = File(...)):
    """Upload and process audio document"""
    try:
        # Transcribe audio
        transcription = process_audio(file.file)
        
        # Get embedding for transcription
        text_embeddings, _ = get_embeddings([transcription])
        
        # Store document
        doc_id = f"audio_{len(documents)}"
        documents.append({
            "id": doc_id,
            "content": f"Audio transcription: {transcription}",
            "modality": "audio",
            "filename": file.filename,
            "transcription": transcription
        })
        embeddings.append(text_embeddings[0])
        
        return {
            "message": "Audio document uploaded successfully", 
            "doc_id": doc_id,
            "transcription": transcription
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=RAGResponse)
async def query_documents(request: QueryRequest):
    """Query documents using multimodal RAG"""
    try:
        if not documents:
            return RAGResponse(
                answer="No documents available. Please upload some documents first.",
                relevant_documents=[]
            )
        
        # Get query embedding
        query_embeddings, _ = get_embeddings([request.query])
        query_embedding = query_embeddings[0]
        
        # Calculate similarities
        doc_embeddings = torch.stack(embeddings)
        similarities = calculate_similarity(query_embedding, doc_embeddings)
        
        # Get top 3 most similar documents
        top_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)[:3]
        
        relevant_docs = []
        for idx in top_indices:
            relevant_docs.append(DocumentResponse(
                id=documents[idx]["id"],
                content=documents[idx]["content"],
                modality=documents[idx]["modality"],
                similarity_score=similarities[idx]
            ))
        
        # Simple RAG response (in a real system, you'd use a proper LLM)
        if relevant_docs:
            top_doc = relevant_docs[0]
            answer = f"Based on the most relevant document ({top_doc.modality}), here's what I found: {top_doc.content[:200]}..."
        else:
            answer = "No relevant documents found for your query."
        
        return RAGResponse(
            answer=answer,
            relevant_documents=relevant_docs
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def get_documents():
    """Get all uploaded documents"""
    return {"documents": documents}

@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a specific document"""
    try:
        for i, doc in enumerate(documents):
            if doc["id"] == doc_id:
                documents.pop(i)
                embeddings.pop(i)
                return {"message": f"Document {doc_id} deleted successfully"}
        raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
