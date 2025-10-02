#!/bin/bash

# Push All Feature Branches Script
echo "🚀 Pushing all feature branches to remote..."

# List of feature branches
branches=(
    "feature/ai-models-integration"
    "feature/backend-api-development"
    "feature/frontend-ui-components"
    "feature/vector-database-implementation"
    "feature/rag-architecture-implementation"
    "feature/documentation-and-setup"
)

# Push each branch
for branch in "${branches[@]}"; do
    echo "📤 Pushing $branch..."
    git push origin $branch
    if [ $? -eq 0 ]; then
        echo "✅ $branch pushed successfully"
    else
        echo "❌ Failed to push $branch"
    fi
    echo ""
done

echo "🎉 All branches pushed!"
echo "📋 Next steps:"
echo "1. Go to GitHub repository"
echo "2. Create Pull Requests for each branch"
echo "3. Use the PR templates from create_prs.md"
echo "4. Review and merge in dependency order"

