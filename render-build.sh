#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Ghostscript (Required for Camelot)
apt-get update && apt-get install -y ghostscript python3-tk

# Install Python dependencies
pip install -r requirements.txt