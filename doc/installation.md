# Installation Guide

## Prerequisites

- Python 3.8 or higher
- CUDA-compatible GPU (recommended for optimal performance)
- 8GB RAM minimum (16GB recommended)

## Basic Installation

```bash
# Clone the repository
git clone https://github.com/JJshome/GridShapeAI.git
cd GridShapeAI

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## GPU Support

For better performance, make sure you have the appropriate CUDA drivers installed for your GPU. The system will automatically detect and use available GPU resources.

## Verification

Verify your installation by running the test script:

```bash
python src/test_installation.py
```

If everything is set up correctly, you should see a confirmation message and a simple shape generation example.