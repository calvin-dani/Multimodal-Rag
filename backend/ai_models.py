"""
AI Models Integration Module
Handles CLIP and Speech2Text model loading and processing
"""

import torch
from transformers import CLIPProcessor, CLIPModel, Speech2TextProcessor, Speech2TextForConditionalGeneration
import numpy as np
from PIL import Image
from typing import List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIModelsManager:
    """Manages AI models for multimodal processing"""
    
    def __init__(self):
        self.clip_model = None
        self.clip_processor = None
        self.speech_model = None
        self.speech_processor = None
        self.models_loaded = False
    
    def load_models(self) -> bool:
        """Load CLIP and Speech2Text models"""
        try:
            logger.info("Loading CLIP model...")
            self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
            self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
            
            logger.info("Loading Speech2Text model...")
            self.speech_model = Speech2TextForConditionalGeneration.from_pretrained("facebook/s2t-medium-librispeech-asr")
            self.speech_processor = Speech2TextProcessor.from_pretrained("facebook/s2t-medium-librispeech-asr")
            
            self.models_loaded = True
            logger.info("All AI models loaded successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error loading AI models: {e}")
            return False
    
    def get_text_embeddings(self, texts: List[str]) -> torch.Tensor:
        """Get text embeddings using CLIP"""
        if not self.models_loaded:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        
        inputs = self.clip_processor(text=texts, return_tensors="pt", padding=True)
        with torch.no_grad():
            text_embeddings = self.clip_model.get_text_features(**inputs)
        return text_embeddings
    
    def get_image_embeddings(self, images: List[Image.Image]) -> torch.Tensor:
        """Get image embeddings using CLIP"""
        if not self.models_loaded:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        
        inputs = self.clip_processor(images=images, return_tensors="pt")
        with torch.no_grad():
            image_embeddings = self.clip_model.get_image_features(**inputs)
        return image_embeddings
    
    def transcribe_audio(self, audio_waveform: np.ndarray, sampling_rate: int = 16000) -> str:
        """Transcribe audio using Speech2Text model"""
        if not self.models_loaded:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        
        inputs = self.speech_processor(audio_waveform, sampling_rate=sampling_rate, return_tensors="pt")
        with torch.no_grad():
            generated_ids = self.speech_model.generate(
                inputs["input_features"], 
                attention_mask=inputs["attention_mask"]
            )
        
        transcription = self.speech_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return transcription
    
    def get_unified_embeddings(self, texts: List[str] = None, images: List[Image.Image] = None) -> Tuple[Optional[torch.Tensor], Optional[torch.Tensor]]:
        """Get unified embeddings for texts and images"""
        text_embeddings = None
        image_embeddings = None
        
        if texts:
            text_embeddings = self.get_text_embeddings(texts)
        
        if images:
            image_embeddings = self.get_image_embeddings(images)
        
        return text_embeddings, image_embeddings
    
    def is_ready(self) -> bool:
        """Check if models are loaded and ready"""
        return self.models_loaded

# Global instance
ai_models = AIModelsManager()
