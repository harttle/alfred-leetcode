#!/bin/bash
set -e

# Check for version argument
if [ "$1" == "--version" ] || [ "$1" == "-v" ]; then
    if [ -z "$2" ]; then
        echo "Error: Version argument is missing"
        echo "Usage: $0 --version VERSION"
        exit 1
    fi
    VERSION="$2"
    echo "Building release version: $VERSION (manually specified)"
else
    # For local development/testing, use default version
    VERSION="1.0.0-dev"
    echo "Building test version: $VERSION (default for local development)"
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