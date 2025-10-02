"""
Test script for Backend API Endpoints
Tests FastAPI endpoints and functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pytest
import asyncio
from fastapi.testclient import TestClient
from api_endpoints import app, documents, embeddings
import io
from PIL import Image

# Create test client
client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "models_loaded" in data
    assert "documents_count" in data

def test_upload_text():
    """Test text upload endpoint"""
    # Create a test text file
    test_content = "This is a test document for API testing."
    files = {"file": ("test.txt", test_content, "text/plain")}
    
    response = client.post("/upload/text", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "doc_id" in data

def test_upload_image():
    """Test image upload endpoint"""
    # Create a test image
    test_image = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    test_image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    files = {"file": ("test.jpg", img_byte_arr, "image/jpeg")}
    
    response = client.post("/upload/image", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "doc_id" in data

def test_query_documents():
    """Test document query endpoint"""
    # First upload a test document
    test_content = "This is a test document about artificial intelligence."
    files = {"file": ("test.txt", test_content, "text/plain")}
    client.post("/upload/text", files=files)
    
    # Now query
    query_data = {"query": "What is artificial intelligence?"}
    response = client.post("/query", json=query_data)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "relevant_documents" in data

def test_get_documents():
    """Test get documents endpoint"""
    response = client.get("/documents")
    assert response.status_code == 200
    data = response.json()
    assert "documents" in data
    assert isinstance(data["documents"], list)

def test_delete_document():
    """Test delete document endpoint"""
    # First upload a test document
    test_content = "This is a test document for deletion."
    files = {"file": ("test_delete.txt", test_content, "text/plain")}
    upload_response = client.post("/upload/text", files=files)
    doc_id = upload_response.json()["doc_id"]
    
    # Now delete it
    response = client.delete(f"/documents/{doc_id}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

def test_delete_nonexistent_document():
    """Test deleting non-existent document"""
    response = client.delete("/documents/nonexistent")
    assert response.status_code == 404

def test_query_empty_documents():
    """Test querying when no documents exist"""
    # Clear documents for this test
    global documents, embeddings
    original_docs = documents.copy()
    original_embeddings = embeddings.copy()
    
    documents.clear()
    embeddings.clear()
    
    query_data = {"query": "test query"}
    response = client.post("/query", json=query_data)
    assert response.status_code == 200
    data = response.json()
    assert "No documents available" in data["answer"]
    
    # Restore original state
    documents.extend(original_docs)
    embeddings.extend(original_embeddings)

def run_tests():
    """Run all API tests"""
    print("🧪 Running Backend API Tests...")
    print("=" * 50)
    
    tests = [
        test_root_endpoint,
        test_health_endpoint,
        test_upload_text,
        test_upload_image,
        test_query_documents,
        test_get_documents,
        test_delete_document,
        test_delete_nonexistent_document,
        test_query_empty_documents
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All API tests passed!")
        return True
    else:
        print("⚠️ Some tests failed. Check the output above.")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
