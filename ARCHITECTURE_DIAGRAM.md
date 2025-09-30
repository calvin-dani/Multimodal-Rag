# Multimodal RAG System - Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    MULTIMODAL RAG SYSTEM                                        │
│                                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                                USER INTERFACE LAYER                                     │   │
│  │                                                                                         │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │   │
│  │  │   File Upload   │  │   Query Input   │  │  Results View   │  │ Document Mgmt   │   │   │
│  │  │   Components    │  │   Components    │  │   Components    │  │   Components    │   │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘   │   │
│  │           │                     │                     │                     │           │   │
│  │           ▼                     ▼                     ▼                     ▼           │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────────────┐   │   │
│  │  │                        React Frontend (Port 3000)                              │   │   │
│  │  │  • Drag & Drop Uploads  • Real-time UI  • Responsive Design  • Error Handling │   │   │
│  │  └─────────────────────────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                           │                                                   │
│                                           │ HTTP/HTTPS                                        │
│                                           ▼                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                                API GATEWAY LAYER                                      │   │
│  │                                                                                         │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────────────┐   │   │
│  │  │                        FastAPI Backend (Port 8000)                             │   │   │
│  │  │                                                                                 │   │   │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │   │   │
│  │  │  │   Upload    │  │   Query     │  │  Document   │  │   Health    │           │   │   │
│  │  │  │  Endpoints  │  │ Endpoints   │  │ Management  │  │   Checks    │           │   │   │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘           │   │   │
│  │  │                                                                                 │   │   │
│  │  │  ┌─────────────────────────────────────────────────────────────────────────┐   │   │   │
│  │  │  │                    Request Processing Pipeline                        │   │   │   │
│  │  │  │  • File Validation  • CORS Handling  • Error Management  • Logging   │   │   │   │
│  │  │  └─────────────────────────────────────────────────────────────────────────┘   │   │   │
│  │  └─────────────────────────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                           │                                                   │
│                                           ▼                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                              PROCESSING LAYER                                         │   │
│  │                                                                                         │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │   │
│  │  │   Text          │  │   Image         │  │   Audio         │  │   Vector        │   │   │
│  │  │  Processor      │  │  Processor      │  │  Processor      │  │  Generator      │   │   │
│  │  │                 │  │                 │  │                 │  │                 │   │   │
│  │  │ • Direct        │  │ • PIL Image     │  │ • PyDub         │  │ • CLIP Model    │   │   │
│  │  │   Processing    │  │   Processing    │  │   Conversion    │  │ • Embedding     │   │   │
│  │  │ • UTF-8         │  │ • Format        │  │ • FFmpeg        │  │   Generation    │   │   │
│  │  │   Encoding      │  │   Validation    │  │   Processing    │  │ • 512-dim       │   │   │
│  │  │ • Text          │  │ • Resize        │  │ • Speech2Text   │  │   Vectors       │   │   │
│  │  │   Extraction    │  │   Normalize     │  │   Transcription │  │                 │   │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                           │                                                   │
│                                           ▼                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                              AI MODEL LAYER                                           │   │
│  │                                                                                         │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────────────┐   │   │
│  │  │                            CLIP Model                                          │   │   │
│  │  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │   │   │
│  │  │  │   Text          │  │   Vision        │  │   Contrastive   │                │   │   │
│  │  │  │   Encoder       │  │   Encoder       │  │   Learning      │                │   │   │
│  │  │  │                 │  │                 │  │                 │                │   │   │
│  │  │  │ • Transformer   │  │ • ViT-Base      │  │ • Cross-modal   │                │   │   │
│  │  │  │   Architecture  │  │   Architecture  │  │   Alignment     │                │   │   │
│  │  │  │ • 512-dim       │  │ • 512-dim       │  │ • Similarity    │                │   │   │
│  │  │  │   Output        │  │   Output        │  │   Learning      │                │   │   │
│  │  │  └─────────────────┘  └─────────────────┘  └─────────────────┘                │   │   │
│  │  └─────────────────────────────────────────────────────────────────────────────────┘   │   │
│  │                                                                                         │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────────────┐   │   │
│  │  │                        Speech2Text Model                                       │   │   │
│  │  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │   │   │
│  │  │  │   Audio         │  │   Encoder-      │  │   Text          │                │   │   │
│  │  │  │   Preprocessing │  │   Decoder       │  │   Generation    │                │   │   │
│  │  │  │                 │  │                 │  │                 │                │   │   │
│  │  │  │ • 16kHz         │  │ • Transformer   │  │ • Beam Search   │                │   │   │
│  │  │  │   Sampling      │  │   Architecture  │  │ • Tokenization  │                │   │   │
│  │  │  │ • Feature       │  │ • Attention     │  │ • Decoding      │                │   │   │
│  │  │  │   Extraction    │  │   Mechanism     │  │                 │                │   │   │
│  │  │  └─────────────────┘  └─────────────────┘  └─────────────────┘                │   │   │
│  │  └─────────────────────────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                           │                                                   │
│                                           ▼                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                              STORAGE LAYER                                            │   │
│  │                                                                                         │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────────────┐   │   │
│  │  │                        Vector Database (In-Memory)                              │   │   │
│  │  │                                                                                 │   │   │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │   │   │
│  │  │  │   Vector    │  │   Document  │  │   Metadata  │  │   Search    │           │   │   │
│  │  │  │   Storage   │  │   Index     │  │   Storage   │  │   Index     │           │   │   │
│  │  │  │             │  │             │  │             │  │             │           │   │   │
│  │  │  │ • PyTorch   │  │ • Document  │  │ • File Info │  │ • Cosine    │           │   │   │
│  │  │  │   Tensors   │  │   IDs       │  │ • Modality  │  │   Similarity│           │   │   │
│  │  │  │ • 512-dim   │  │ • Timestamps│  │ • Filename  │  │ • Ranking   │           │   │   │
│  │  │  │   Vectors   │  │ • Ordering  │  │ • Size      │  │ • Top-K     │           │   │   │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘           │   │   │
│  │  └─────────────────────────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA FLOW PROCESSING                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Upload    │    │  Preprocess │    │   Embed     │    │   Store     │     │
│  │   Files     │───►│   & Parse   │───►│   Vectors   │───►│   Vectors   │     │
│  │             │    │             │    │             │    │             │     │
│  │ • Text      │    │ • Validate  │    │ • CLIP      │    │ • In-Memory │     │
│  │ • Image     │    │ • Convert   │    │   Encoding  │    │ • Index     │     │
│  │ • Audio     │    │ • Normalize │    │ • 512-dim   │    │ • Metadata  │     │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Query     │    │   Encode    │    │   Search    │    │  Retrieve   │     │
│  │   Input     │───►│   Query     │───►│   Vectors   │───►│   Results   │     │
│  │             │    │             │    │             │    │             │     │
│  │ • Natural   │    │ • CLIP      │    │ • Cosine    │    │ • Ranked    │     │
│  │   Language  │    │   Encoding  │    │   Similarity│    │   Results   │     │
│  │ • Keywords  │    │ • 512-dim   │    │ • Top-K     │    │ • Metadata  │     │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Model Architecture Details

### CLIP Model Architecture
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CLIP ARCHITECTURE                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────┐    ┌─────────────────────────────────┐     │
│  │         TEXT ENCODER            │    │        VISION ENCODER           │     │
│  │                                 │    │                                 │     │
│  │  Input Text                     │    │  Input Image                    │     │
│  │       │                         │    │       │                         │     │
│  │       ▼                         │    │       ▼                         │     │
│  │  Tokenization                   │    │  Patch Embedding                │     │
│  │       │                         │    │       │                         │     │
│  │       ▼                         │    │       ▼                         │     │
│  │  Positional Encoding            │    │  Positional Encoding            │     │
│  │       │                         │    │       │                         │     │
│  │       ▼                         │    │       ▼                         │     │
│  │  Transformer Layers             │    │  Transformer Layers             │     │
│  │  (12 layers)                    │    │  (12 layers)                    │     │
│  │       │                         │    │       │                         │     │
│  │       ▼                         │    │       ▼                         │     │
│  │  Layer Normalization            │    │  Layer Normalization            │     │
│  │       │                         │    │       │                         │     │
│  │       ▼                         │    │       ▼                         │     │
│  │  Text Features (512-dim)        │    │  Image Features (512-dim)       │     │
│  └─────────────────────────────────┘    └─────────────────────────────────┘     │
│                    │                                        │                   │
│                    └────────────────┬───────────────────────┘                   │
│                                     ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐     │
│  │                        CONTRASTIVE LEARNING                            │     │
│  │                                                                         │     │
│  │  • Cosine Similarity Calculation                                       │     │
│  │  • Cross-Modal Alignment                                               │     │
│  │  • Contrastive Loss Optimization                                       │     │
│  │  • Unified Embedding Space (512-dim)                                   │     │
│  └─────────────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Speech2Text Model Architecture
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          SPEECH2TEXT ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐     │
│  │                            ENCODER                                    │     │
│  │                                                                         │     │
│  │  Audio Input (16kHz)                                                   │     │
│  │       │                                                                 │     │
│  │       ▼                                                                 │     │
│  │  Feature Extraction                                                     │     │
│  │  • Mel-spectrogram                                                      │     │
│  │  • 80 mel-frequency bins                                                │     │
│  │       │                                                                 │     │
│  │       ▼                                                                 │     │
│  │  Convolutional Layers                                                   │     │
│  │  • 2D Convolutions                                                      │     │
│  │  • Batch Normalization                                                 │     │
│  │       │                                                                 │     │
│  │       ▼                                                                 │     │
│  │  Transformer Encoder                                                    │     │
│  │  • 16 layers                                                            │     │
│  │  • Multi-head attention                                                 │     │
│  │  • Feed-forward networks                                               │     │
│  │       │                                                                 │     │
│  │       ▼                                                                 │     │
│  │  Encoder Output                                                         │     │
│  └─────────────────────────────────────────────────────────────────────────┘     │
│                                     │                                           │
│                                     ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐     │
│  │                            DECODER                                    │     │
│  │                                                                         │     │
│  │  Encoder Output + Previous Tokens                                      │     │
│  │       │                                                                 │     │
│  │       ▼                                                                 │     │
│  │  Transformer Decoder                                                    │     │
│  │  • 6 layers                                                             │     │
│  │  • Self-attention                                                       │     │
│  │  • Cross-attention                                                      │     │
│  │       │                                                                 │     │
│  │       ▼                                                                 │     │
│  │  Linear Projection                                                      │     │
│  │       │                                                                 │     │
│  │       ▼                                                                 │     │
│  │  Text Output                                                            │     │
│  └─────────────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Performance Characteristics

### Model Performance
- **CLIP Model Size**: ~600MB
- **Speech2Text Model Size**: ~600MB
- **Total Model Memory**: ~1.2GB
- **Inference Speed**: 
  - Text: ~50ms per document
  - Image: ~200ms per image
  - Audio: ~1-3s per minute

### System Requirements
- **Minimum RAM**: 4GB
- **Recommended RAM**: 8GB+
- **CPU**: Multi-core recommended
- **Storage**: 2GB for models + documents
- **Network**: Internet for initial model download

### Scalability Limits
- **Current**: ~1000 documents (in-memory)
- **Recommended**: ~100 documents for optimal performance
- **Bottleneck**: Memory usage with large document sets
