#!/bin/bash
set -e

# Determine version - use GITHUB_REF_NAME in CI or hardcoded for local testing
if [ -n "$GITHUB_REF_NAME" ]; then
    # In GitHub Actions, the ref name will be the tag (e.g., v1.2.0)
    # Remove the 'v' prefix if present
    VERSION=${GITHUB_REF_NAME#v}
    echo "Building release version: $VERSION (from GitHub CI)"
else
    # For local development/testing, use hardcoded version
    VERSION="1.0.0-dev"
    echo "Building test version: $VERSION (hardcoded for local development)"
fi

# Output filename
WORKFLOW_FILE="alfred-leetcode.alfredworkflow"

# Clean up previous build artifacts
rm -rf workflow
rm -f "$WORKFLOW_FILE"

# Create workflow directory and prepare files
mkdir -p workflow
SCRIPT_FILTER_UID=$(uuidgen | tr "[:lower:]" "[:upper:]")
BROWSER_OPENER_UID=$(uuidgen | tr "[:lower:]" "[:upper:]")

# Copy the Python script and requirements
cp alfred_leetcode.py requirements.txt workflow/

# Copy LeetCode icon to workflow directory
cp assets/leetcode-icon.png workflow/icon.png

# Install dependencies 
echo "Installing dependencies to workflow directory..."
pip3 install -r requirements.txt --target workflow/

# Generate workflow configuration using the template
echo "Generating workflow info.plist..."
sed -e "s/SCRIPT_FILTER_UID/$SCRIPT_FILTER_UID/g" \
    -e "s/BROWSER_OPENER_UID/$BROWSER_OPENER_UID/g" \
    -e "s/VERSION_PLACEHOLDER/$VERSION/g" \
    info.plist.template > workflow/info.plist

# Create workflow package
echo "Creating workflow package..."
cd workflow && zip -r "../$WORKFLOW_FILE" * && cd ..

echo "✅ $WORKFLOW_FILE version $VERSION created successfully."
echo "You can now install the workflow by double-clicking the workflow file." 