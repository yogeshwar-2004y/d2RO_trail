#!/bin/bash

# Script to fix all hardcoded localhost:8000 URLs in the frontend
# Run this from the Aviatrax directory

cd frontend/src

echo "Fixing hardcoded URLs..."

# Replace http://localhost:8000/api with /api
find . -type f \( -name "*.vue" -o -name "*.js" \) -exec sed -i 's|http://localhost:8000/api|/api|g' {} +

# Replace http://127.0.0.1:8000/api with /api
find . -type f \( -name "*.vue" -o -name "*.js" \) -exec sed -i 's|http://127.0.0.1:8000/api|/api|g' {} +

# Replace http://localhost:8000/ with / (for any other localhost:8000 references)
find . -type f \( -name "*.vue" -o -name "*.js" \) -exec sed -i 's|http://localhost:8000/|/|g' {} +

# Replace http://127.0.0.1:8000/ with / (for any other 127.0.0.1:8000 references)
find . -type f \( -name "*.vue" -o -name "*.js" \) -exec sed -i 's|http://127.0.0.1:8000/|/|g' {} +

echo "✅ All URLs fixed!"
echo "Files modified. Please review the changes before committing."

