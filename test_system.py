#!/usr/bin/env python3
"""
Test script for Multimodal RAG system
This script tests the backend API endpoints
"""

import requests
import json
import time
import os

API_BASE_URL = "http://localhost:8000"

def test_api_health():
    """Test if the API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            print("✅ API is running")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the backend is running.")
        return False

def test_text_upload():
    """Test text document upload"""
    print("\n📝 Testing text upload...")
    
    # Create a test text file
    test_content = "This is a test document about artificial intelligence and machine learning."
    
    files = {'file': ('test.txt', test_content, 'text/plain')}
    
    try:
        response = requests.post(f"{API_BASE_URL}/upload/text", files=files)
        if response.status_code == 200:
            print("✅ Text upload successful")
            return response.json().get('doc_id')
        else:
            print(f"❌ Text upload failed: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Text upload error: {e}")
        return None

def test_image_upload():
    """Test image document upload"""
    print("\n🖼️ Testing image upload...")
    
    # Create a simple test image
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (100, 100), color='red')
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), "TEST", fill='white')
    
    # Save to bytes
    import io
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    files = {'file': ('test.jpg', img_bytes, 'image/jpeg')}
    
    try:
        response = requests.post(f"{API_BASE_URL}/upload/image", files=files)
        if response.status_code == 200:
            print("✅ Image upload successful")
            return response.json().get('doc_id')
        else:
            print(f"❌ Image upload failed: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Image upload error: {e}")
        return None

def test_query():
    """Test document querying"""
    print("\n🔍 Testing query...")
    
    query_data = {
        "query": "What is artificial intelligence?"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/query", json=query_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Query successful")
            print(f"Answer: {result.get('answer', 'No answer')}")
            print(f"Relevant documents: {len(result.get('relevant_documents', []))}")
            return True
        else:
            print(f"❌ Query failed: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Query error: {e}")
        return False

def test_documents_list():
    """Test getting documents list"""
    print("\n📋 Testing documents list...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/documents")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Documents list retrieved: {len(result.get('documents', []))} documents")
            return True
        else:
            print(f"❌ Documents list failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Documents list error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Multimodal RAG System")
    print("=" * 40)
    
    # Test API health
    if not test_api_health():
        print("\n❌ API is not running. Please start the backend first:")
        print("python backend/main.py")
        return
    
    # Test uploads
    text_doc_id = test_text_upload()
    image_doc_id = test_image_upload()
    
    # Wait a moment for processing
    time.sleep(2)
    
    # Test querying
    test_query()
    
    # Test documents list
    test_documents_list()
    
    print("\n" + "=" * 40)
    print("✅ All tests completed!")
    print("\nTo test the full system:")
    print("1. Start the backend: python backend/main.py")
    print("2. Start the frontend: cd frontend && npm start")
    print("3. Open http://localhost:3000 in your browser")

if __name__ == "__main__":
    main()
