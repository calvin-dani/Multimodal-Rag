import React, { useState, useEffect } from 'react';
import { Upload, FileText, Image, Mic, Search, Trash2, Loader } from 'lucide-react';
import axios from 'axios';
import './index.css';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [documents, setDocuments] = useState([]);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Load documents on component mount
  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/documents`);
      setDocuments(response.data.documents);
    } catch (error) {
      console.error('Error loading documents:', error);
    }
  };

  const uploadFile = async (file, type) => {
    setLoading(true);
    setMessage('');
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      let endpoint = '';
      switch (type) {
        case 'text':
          endpoint = '/upload/text';
          break;
        case 'image':
          endpoint = '/upload/image';
          break;
        case 'audio':
          endpoint = '/upload/audio';
          break;
        default:
          throw new Error('Invalid file type');
      }
      
      const response = await axios.post(`${API_BASE_URL}${endpoint}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      setMessage(`✅ ${response.data.message}`);
      loadDocuments(); // Reload documents
    } catch (error) {
      setMessage(`❌ Error uploading file: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = (event, type) => {
    const file = event.target.files[0];
    if (file) {
      uploadFile(file, type);
    }
  };

  const handleDrop = (event, type) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file) {
      uploadFile(file, type);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const queryDocuments = async () => {
    if (!query.trim()) {
      setMessage('Please enter a query');
      return;
    }
    
    setLoading(true);
    setMessage('');
    
    try {
      const response = await axios.post(`${API_BASE_URL}/query`, {
        query: query.trim()
      });
      
      setResults(response.data);
      setMessage('✅ Query completed successfully');
    } catch (error) {
      setMessage(`❌ Error querying documents: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const deleteDocument = async (docId) => {
    try {
      await axios.delete(`${API_BASE_URL}/documents/${docId}`);
      setMessage('✅ Document deleted successfully');
      loadDocuments(); // Reload documents
    } catch (error) {
      setMessage(`❌ Error deleting document: ${error.response?.data?.detail || error.message}`);
    }
  };

  const UploadZone = ({ type, icon, title, subtitle, accept }) => (
    <div
      className="upload-zone"
      onDrop={(e) => handleDrop(e, type)}
      onDragOver={handleDragOver}
      onClick={() => document.getElementById(`${type}-input`).click()}
    >
      <div className="upload-icon">{icon}</div>
      <div className="upload-text">{title}</div>
      <div className="upload-subtext">{subtitle}</div>
      <input
        id={`${type}-input`}
        type="file"
        className="file-input"
        accept={accept}
        onChange={(e) => handleFileUpload(e, type)}
      />
    </div>
  );

  return (
    <div className="container">
      <div className="header">
        <h1>Multimodal RAG</h1>
        <p>Upload and query text, images, and audio documents using AI</p>
      </div>

      {message && (
        <div className={message.includes('❌') ? 'error' : 'success'}>
          {message}
        </div>
      )}

      <div className="card">
        <h2>Upload Documents</h2>
        <div className="upload-section">
          <UploadZone
            type="text"
            icon={<FileText />}
            title="Upload Text"
            subtitle="Upload .txt, .md, .pdf files"
            accept=".txt,.md,.pdf"
          />
          <UploadZone
            type="image"
            icon={<Image />}
            title="Upload Image"
            subtitle="Upload .jpg, .png, .gif files"
            accept=".jpg,.jpeg,.png,.gif"
          />
          <UploadZone
            type="audio"
            icon={<Mic />}
            title="Upload Audio"
            subtitle="Upload .mp3, .wav, .m4a files"
            accept=".mp3,.wav,.m4a"
          />
        </div>
      </div>

      <div className="card">
        <h2>Query Documents</h2>
        <div className="query-section">
          <input
            type="text"
            className="query-input"
            placeholder="Ask a question about your uploaded documents..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && queryDocuments()}
          />
          <button
            className="query-button"
            onClick={queryDocuments}
            disabled={loading || !query.trim()}
          >
            {loading ? <Loader className="spinner" /> : <Search />}
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>

        {results && (
          <div className="results-section">
            <h3>Answer</h3>
            <div className="result-card">
              <div className="result-content">{results.answer}</div>
            </div>

            <h3>Relevant Documents</h3>
            {results.relevant_documents.map((doc, index) => (
              <div key={index} className="result-card">
                <div className="result-header">
                  <span className="result-modality">{doc.modality}</span>
                  <span className="result-score">
                    Similarity: {(doc.similarity_score * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="result-content">{doc.content}</div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="card">
        <h2>Uploaded Documents ({documents.length})</h2>
        <div className="documents-section">
          {documents.length === 0 ? (
            <p className="loading">No documents uploaded yet</p>
          ) : (
            documents.map((doc) => (
              <div key={doc.id} className="document-item">
                <div className="document-info">
                  <span className="document-modality">{doc.modality}</span>
                  <span>{doc.filename || doc.id}</span>
                </div>
                <button
                  className="delete-button"
                  onClick={() => deleteDocument(doc.id)}
                >
                  <Trash2 size={16} />
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
