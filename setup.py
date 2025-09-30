#!/usr/bin/env python3
"""
Setup script for Multimodal RAG system
This script helps set up the environment and download sample data
"""

import os
import sys
import subprocess
import requests
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_sample_image():
    """Create a sample image for testing"""
    # Create a simple image with text
    img = Image.new('RGB', (400, 300), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add some text
    try:
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        font = None
    
    text = "Sample Image\nMultimodal RAG\nTest Document"
    draw.text((50, 100), text, fill='black', font=font)
    
    # Add some shapes
    draw.rectangle([50, 200, 350, 250], outline='blue', width=3)
    draw.ellipse([150, 50, 250, 100], outline='red', width=2)
    
    # Save the image
    img_path = 'sample_data/sample_image.jpg'
    img.save(img_path)
    print(f"✅ Created sample image: {img_path}")
    return img_path

def download_sample_audio():
    """Download or create a sample audio file"""
    # For now, we'll create a simple text file that represents audio transcription
    # In a real implementation, you would download actual audio files
    audio_text = """
    This is a sample audio transcription for testing the multimodal RAG system.
    The audio contains information about various topics that can be searched.
    
    Topics covered:
    - Technology and artificial intelligence
    - Literature and books
    - Music and composers
    - Science and mathematics
    - History and culture
    
    This demonstrates how audio content can be converted to text and then
    embedded using the same CLIP model used for text documents.
    """
    
    with open('sample_data/sample_audio_transcription.txt', 'w') as f:
        f.write(audio_text)
    
    print("✅ Created sample audio transcription file")
    return 'sample_data/sample_audio_transcription.txt'

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python requirements...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Python requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def setup_frontend():
    """Setup React frontend"""
    print("📦 Setting up React frontend...")
    try:
        os.chdir('frontend')
        subprocess.check_call(['npm', 'install'])
        print("✅ Frontend dependencies installed successfully")
        os.chdir('..')
    except subprocess.CalledProcessError as e:
        print(f"❌ Error setting up frontend: {e}")
        return False
    return True

def create_directories():
    """Create necessary directories"""
    directories = [
        'sample_data',
        'backend',
        'frontend/src',
        'frontend/public'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def main():
    """Main setup function"""
    print("🚀 Setting up Multimodal RAG System...")
    print("=" * 50)
    
    # Create directories
    create_directories()
    
    # Install Python requirements
    if not install_requirements():
        print("❌ Setup failed at requirements installation")
        return
    
    # Setup frontend
    if not setup_frontend():
        print("❌ Setup failed at frontend setup")
        return
    
    # Create sample data
    print("\n📁 Creating sample data...")
    create_sample_image()
    download_sample_audio()
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\nTo run the system:")
    print("1. Start the backend: python backend/main.py")
    print("2. Start the frontend: cd frontend && npm start")
    print("3. Open http://localhost:3000 in your browser")
    print("\nSample files are available in the sample_data/ directory")

if __name__ == "__main__":
    main()
