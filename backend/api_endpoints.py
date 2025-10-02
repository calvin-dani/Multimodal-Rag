"""
Backend API Endpoints Module
Handles FastAPI endpoints for multimodal document processing
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
from ai_models import ai_models

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for request/response
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

class HealthResponse(BaseModel):
    status: str
    models_loaded: bool
    documents_count: int

# Global storage (in production, use a proper database)
documents = []
embeddings = []

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="Multimodal RAG API",
        description="API for multimodal document retrieval and search",
        version="1.0.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app

# Create FastAPI app
app = create_app()

@app.on_event("startup")
async def startup_event():
    """Initialize AI models on startup"""
    logger.info("Starting up Multimodal RAG API...")
    success = ai_models.load_models()
    if not success:
        logger.error("Failed to load AI models")
        raise RuntimeError("Could not load AI models")

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {"message": "Multimodal RAG API is running!"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        models_loaded=ai_models.is_ready(),
        documents_count=len(documents)
    )

@app.post("/upload/text")
async def upload_text(file: UploadFile = File(...)):
    """Upload and process text document"""
    try:
        content = await file.read()
        text_content = content.decode('utf-8')
        
        # Get embedding using AI models
        text_embeddings = ai_models.get_text_embeddings([text_content])
        
        # Store document
        doc_id = f"text_{len(documents)}"
        documents.append({
            "id": doc_id,
            "content": text_content,
            "modality": "text",
            "filename": file.filename
        })
        embeddings.append(text_embeddings[0])
        
        logger.info(f"Text document uploaded: {doc_id}")
        return {"message": "Text document uploaded successfully", "doc_id": doc_id}
        
    except Exception as e:
        logger.error(f"Error uploading text: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    """Upload and process image document"""
    try:
        from PIL import Image
        import io
        
        content = await file.read()
        image = Image.open(io.BytesIO(content))
        
        # Get embedding using AI models
        image_embeddings = ai_models.get_image_embeddings([image])
        
        # Store document
        doc_id = f"image_{len(documents)}"
        documents.append({
            "id": doc_id,
            "content": f"Image: {file.filename}",
            "modality": "image",
            "filename": file.filename
        })
        embeddings.append(image_embeddings[0])
        
        logger.info(f"Image document uploaded: {doc_id}")
        return {"message": "Image document uploaded successfully", "doc_id": doc_id}
        
    except Exception as e:
        logger.error(f"Error uploading image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload/audio")
async def upload_audio(file: UploadFile = File(...)):
    """Upload and process audio document"""
    try:
        from pydub import AudioSegment
        import io
        import numpy as np
        
        # Read and process audio
        content = await file.read()
        audio_segment = AudioSegment.from_file(io.BytesIO(content))
        
        # Downsample to 16000 Hz
        sampling_rate = 16000
        audio_segment = audio_segment.set_frame_rate(sampling_rate)
        
        # Convert to numpy array
        audio_waveform = np.array(audio_segment.get_array_of_samples(), dtype=np.float32)
        
        # Transcribe using AI models
        transcription = ai_models.transcribe_audio(audio_waveform, sampling_rate)
        
        # Get embedding for transcription
        text_embeddings = ai_models.get_text_embeddings([transcription])
        
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
        
        logger.info(f"Audio document uploaded: {doc_id}")
        return {
            "message": "Audio document uploaded successfully", 
            "doc_id": doc_id,
            "transcription": transcription
        }
        
    except Exception as e:
        logger.error(f"Error uploading audio: {e}")
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
        
        # Get query embedding using AI models
        query_embeddings = ai_models.get_text_embeddings([request.query])
        query_embedding = query_embeddings[0]
        
        # Calculate similarities (this would be in vector database module)
        from torch.nn.functional import cosine_similarity
        import torch
        
        doc_embeddings = torch.stack(embeddings)
        similarities = []
        for i in range(doc_embeddings.shape[0]):
            sim = cosine_similarity(
                query_embedding.unsqueeze(0), 
                doc_embeddings[i].unsqueeze(0)
            ).item()
            similarities.append(sim)
        
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
        
        # Simple RAG response
        if relevant_docs:
            top_doc = relevant_docs[0]
            answer = f"Based on the most relevant document ({top_doc.modality}), here's what I found: {top_doc.content[:200]}..."
        else:
            answer = "No relevant documents found for your query."
        
        logger.info(f"Query processed: '{request.query}' -> {len(relevant_docs)} results")
        return RAGResponse(
            answer=answer,
            relevant_documents=relevant_docs
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
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
                logger.info(f"Document deleted: {doc_id}")
                return {"message": f"Document {doc_id} deleted successfully"}
        
        raise HTTPException(status_code=404, detail="Document not found")
        
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
