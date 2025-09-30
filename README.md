# Multimodal RAG System

A modern Retrieval Augmented Generation (RAG) system that can process and query text, images, and audio documents using AI. This implementation is inspired by the comprehensive guide on multimodal RAG systems.

## Features

- **Multimodal Document Processing**: Upload and process text, images, and audio files
- **AI-Powered Search**: Use CLIP embeddings for semantic search across all modalities
- **Speech-to-Text**: Automatic transcription of audio files
- **Modern Web Interface**: Clean, responsive React frontend
- **RESTful API**: FastAPI backend with comprehensive endpoints

## Architecture

The system uses three main approaches to multimodal RAG:

1. **Shared Vector Space**: CLIP model creates embeddings for both text and images in the same vector space
2. **Single Grounded Modality**: Audio is converted to text using speech-to-text, then embedded with CLIP
3. **Unified Retrieval**: All modalities are searched together using cosine similarity

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **CLIP**: OpenAI's vision-language model for embeddings
- **Transformers**: Hugging Face library for speech-to-text
- **PyTorch**: Deep learning framework

### Frontend
- **React**: Modern JavaScript framework
- **Axios**: HTTP client for API communication
- **Lucide React**: Beautiful icons
- **CSS Grid/Flexbox**: Responsive design

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd multimodal-rag
   python setup.py
   ```

2. **Start the backend**:
   ```bash
   python backend/main.py
   ```
   The API will be available at `http://localhost:8000`

3. **Start the frontend** (in a new terminal):
   ```bash
   cd frontend
   npm start
   ```
   The app will be available at `http://localhost:3000`

### Manual Setup

If the automated setup doesn't work:

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install frontend dependencies**:
   ```bash
   cd frontend
   npm install
   ```

3. **Run the system**:
   ```bash
   # Terminal 1 - Backend
   python backend/main.py
   
   # Terminal 2 - Frontend
   cd frontend
   npm start
   ```

## Usage

### Uploading Documents

1. **Text Documents**: Upload `.txt`, `.md`, or `.pdf` files
2. **Images**: Upload `.jpg`, `.png`, or `.gif` files
3. **Audio**: Upload `.mp3`, `.wav`, or `.m4a` files (will be transcribed automatically)

### Querying Documents

1. Enter your question in the search box
2. The system will find the most relevant documents across all modalities
3. View the AI-generated answer and relevant document snippets

### API Endpoints

- `POST /upload/text` - Upload text documents
- `POST /upload/image` - Upload image documents
- `POST /upload/audio` - Upload audio documents
- `POST /query` - Query all documents
- `GET /documents` - List all uploaded documents
- `DELETE /documents/{doc_id}` - Delete a specific document

## Sample Data

The `sample_data/` directory contains example files:
- `sample_text.txt` - Excerpt from "All Quiet on the Western Front"
- `sample_image.jpg` - Generated test image
- `sample_audio_transcription.txt` - Example audio transcription

## How It Works

### 1. Document Processing
- **Text**: Directly embedded using CLIP's text encoder
- **Images**: Processed through CLIP's vision encoder
- **Audio**: Converted to text using Facebook's Speech2Text model, then embedded

### 2. Embedding Generation
All documents are converted to 512-dimensional vectors using the CLIP model, creating a unified embedding space for all modalities.

### 3. Retrieval
When you query the system:
1. Your query is embedded using the same CLIP model
2. Cosine similarity is calculated between your query and all document embeddings
3. The most similar documents are retrieved

### 4. Response Generation
The system combines the query with relevant documents to generate a contextual response.

## Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
# Optional: Add any configuration here
DEBUG=True
LOG_LEVEL=INFO
```

### Model Configuration
The system uses these pre-trained models:
- **CLIP**: `openai/clip-vit-base-patch32`
- **Speech2Text**: `facebook/s2t-medium-librispeech-asr`

To use different models, modify the model loading in `backend/main.py`.

## Troubleshooting

### Common Issues

1. **Model Download Issues**: The first run will download models (~1GB). Ensure stable internet connection.

2. **Memory Issues**: CLIP models require ~2GB RAM. Close other applications if needed.

3. **Audio Processing**: Some audio formats may not be supported. Try converting to WAV format.

4. **CORS Issues**: Ensure the frontend is running on `http://localhost:3000` and backend on `http://localhost:8000`.

### Performance Tips

- Use smaller images (resize to <1024px) for faster processing
- Limit audio files to reasonable lengths (<10 minutes)
- Consider using GPU acceleration for better performance

## Development

### Project Structure
```
multimodal-rag/
├── backend/
│   └── main.py              # FastAPI backend
├── frontend/
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   ├── index.js         # React entry point
│   │   └── index.css        # Styles
│   └── package.json         # Frontend dependencies
├── sample_data/             # Sample files for testing
├── requirements.txt         # Python dependencies
├── setup.py                # Setup script
└── README.md               # This file
```

### Adding New Modalities

To add support for new data types:

1. Add a new upload endpoint in `backend/main.py`
2. Implement processing logic for the new modality
3. Update the frontend to handle the new file type
4. Modify the embedding generation to include the new modality

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Inspired by [Multimodal RAG — Intuitively and Exhaustively Explained](https://iaee.substack.com/p/multimodal-rag-intuitively-and-exhaustively)
- Built with OpenAI's CLIP model
- Uses Hugging Face Transformers library
- React and FastAPI frameworks
