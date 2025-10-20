#!/bin/bash

set -e

echo "Installing bredos-news locally..."

# Determine tap location
TAP_DIR="$(brew --repository)/Library/Taps/bredos/homebrew-news"

# Create tap if it doesn't exist
if [ ! -d "$TAP_DIR" ]; then
    echo "Creating tap bredos/news..."
    brew tap-new bredos/news
fi

# Create Formula directory
mkdir -p "$TAP_DIR/Formula"

# Copy formula
echo "Copying formula to tap..."
cp bredos-news.rb "$TAP_DIR/Formula/"

# Install or reinstall
if brew list bredos/news/bredos-news &>/dev/null; then
    echo "Reinstalling bredos-news..."
    brew reinstall bredos/news/bredos-news
else
    echo "Installing bredos-news..."
    brew install bredos/news/bredos-news
fi

echo "✓ Installation complete!"
echo ""
echo "To start the service:"
echo "  brew services start bredos/news/bredos-news"
echo ""
echo "To test the client:"
echo "  bredos-news --version"
