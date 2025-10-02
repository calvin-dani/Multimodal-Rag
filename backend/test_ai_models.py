"""
Test script for AI Models Integration
Tests CLIP and Speech2Text model functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_models import ai_models
import numpy as np
from PIL import Image
import time

def test_model_loading():
    """Test model loading functionality"""
    print("🧪 Testing AI Models Loading...")
    
    start_time = time.time()
    success = ai_models.load_models()
    load_time = time.time() - start_time
    
    if success:
        print(f"✅ Models loaded successfully in {load_time:.2f} seconds")
        return True
    else:
        print("❌ Failed to load models")
        return False

def test_text_embeddings():
    """Test text embedding generation"""
    print("\n🧪 Testing Text Embeddings...")
    
    test_texts = [
        "This is a test document about artificial intelligence.",
        "Machine learning and deep learning are fascinating topics.",
        "Natural language processing enables computers to understand text."
    ]
    
    try:
        embeddings = ai_models.get_text_embeddings(test_texts)
        print(f"✅ Generated text embeddings: {embeddings.shape}")
        return True
    except Exception as e:
        print(f"❌ Text embedding test failed: {e}")
        return False

def test_image_embeddings():
    """Test image embedding generation"""
    print("\n🧪 Testing Image Embeddings...")
    
    # Create a simple test image
    test_image = Image.new('RGB', (224, 224), color='red')
    
    try:
        embeddings = ai_models.get_image_embeddings([test_image])
        print(f"✅ Generated image embeddings: {embeddings.shape}")
        return True
    except Exception as e:
        print(f"❌ Image embedding test failed: {e}")
        return False

def test_audio_transcription():
    """Test audio transcription (simulated)"""
    print("\n🧪 Testing Audio Transcription...")
    
    # Create a simple audio waveform for testing
    # In real usage, this would come from an audio file
    sample_rate = 16000
    duration = 1  # 1 second
    frequency = 440  # A note
    
    # Generate a simple sine wave
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio_waveform = np.sin(frequency * 2 * np.pi * t).astype(np.float32)
    
    try:
        # Note: This might not work perfectly with synthetic audio
        # but it tests the model loading and processing pipeline
        transcription = ai_models.transcribe_audio(audio_waveform, sample_rate)
        print(f"✅ Audio transcription result: '{transcription}'")
        return True
    except Exception as e:
        print(f"❌ Audio transcription test failed: {e}")
        return False

def test_unified_embeddings():
    """Test unified embedding generation"""
    print("\n🧪 Testing Unified Embeddings...")
    
    test_texts = ["Test text for unified embeddings"]
    test_image = Image.new('RGB', (224, 224), color='blue')
    
    try:
        text_embeddings, image_embeddings = ai_models.get_unified_embeddings(
            texts=test_texts, 
            images=[test_image]
        )
        
        if text_embeddings is not None:
            print(f"✅ Text embeddings: {text_embeddings.shape}")
        if image_embeddings is not None:
            print(f"✅ Image embeddings: {image_embeddings.shape}")
        
        return True
    except Exception as e:
        print(f"❌ Unified embeddings test failed: {e}")
        return False

def main():
    """Run all AI model tests"""
    print("🚀 Starting AI Models Integration Tests")
    print("=" * 50)
    
    tests = [
        test_model_loading,
        test_text_embeddings,
        test_image_embeddings,
        test_audio_transcription,
        test_unified_embeddings
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All AI model tests passed!")
        return True
    else:
        print("⚠️ Some tests failed. Check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

