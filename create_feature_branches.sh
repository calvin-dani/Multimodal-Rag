#!/bin/bash

# Multimodal RAG - Feature Branch Creation Script
# This script creates feature branches for different components

echo "🚀 Creating feature branches for Multimodal RAG project..."

# Feature 1: AI Models Integration
echo "📦 Creating feature/ai-models-integration branch..."
git checkout -b feature/ai-models-integration
git checkout main

# Feature 2: Backend API Development
echo "🔧 Creating feature/backend-api-development branch..."
git checkout -b feature/backend-api-development
git checkout main

# Feature 3: Frontend UI Components
echo "🎨 Creating feature/frontend-ui-components branch..."
git checkout -b feature/frontend-ui-components
git checkout main

# Feature 4: Vector Database Implementation
echo "🗄️ Creating feature/vector-database-implementation branch..."
git checkout -b feature/vector-database-implementation
git checkout main

# Feature 5: RAG Architecture Implementation
echo "🏗️ Creating feature/rag-architecture-implementation branch..."
git checkout -b feature/rag-architecture-implementation
git checkout main

# Feature 6: Documentation and Setup
echo "📚 Creating feature/documentation-and-setup branch..."
git checkout -b feature/documentation-and-setup
git checkout main

echo "✅ All feature branches created successfully!"
echo "📋 Available branches:"
git branch -a

