#!/usr/bin/env python
# Test script to verify GridShapeAI installation

import sys
import torch
import numpy as np
from os import path
from PIL import Image
import matplotlib.pyplot as plt

# Add parent directory to path for imports
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

def check_requirements():
    """Check if all required packages are installed."""
    try:
        # Check torch
        print(f"PyTorch version: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"CUDA version: {torch.version.cuda}")
            print(f"GPU: {torch.cuda.get_device_name(0)}")
        
        # Check numpy
        print(f"NumPy version: {np.__version__}")
        
        # Check PIL
        print(f"PIL version: {Image.__version__}")
        
        # Check matplotlib
        print(f"Matplotlib version: {plt.matplotlib.__version__}")
        
        # Check imports from the package
        from src.grid.grid3d import Grid3D
        from src.model.shape_model import ShapeModel
        print("All basic imports succeeded.")
        return True
    except ImportError as e:
        print(f"Import error: {e}")
        return False

def create_simple_shape():
    """Create a simple shape as a test."""
    try:
        from src.grid.grid3d import Grid3D
        from src.grid.grid_operations import GridOperations
        
        # Create a grid
        grid = Grid3D(size=100)
        
        # Create a shape (a sphere at the center)
        GridOperations.create_sphere(grid, center=(50, 50, 50), radius=30)
        
        # Get sphere points
        points = grid.get_points_above_threshold()
        print(f"Created a sphere with {len(points)} active points.")
        
        # Visualize a slice of the sphere (z=50)
        plt.figure(figsize=(6, 6))
        plt.imshow(grid.get_slice(2, 50).cpu().numpy(), cmap='viridis')
        plt.title('Sphere Cross-section (z=50)')
        plt.colorbar(label='Value')
        plt.savefig('test_shape.png')
        plt.close()
        
        print("Successfully created and visualized a test shape.")
        print(f"Saved visualization to {path.abspath('test_shape.png')}")
        return True
    except Exception as e:
        print(f"Error creating test shape: {e}")
        return False

def main():
    """Main test function."""
    print("\n----- GridShapeAI Installation Test -----\n")
    
    # Check requirements
    print("Checking requirements...")
    if not check_requirements():
        print("\nError: Some requirements are missing!")
        sys.exit(1)
    print("\nAll requirements are satisfied.")
    
    # Create test shape
    print("\nTesting shape creation...")
    if not create_simple_shape():
        print("\nError: Failed to create test shape!")
        sys.exit(1)
    
    print("\n----- Installation Test Successful! -----")
    print("GridShapeAI is properly installed and ready to use.")
    print("\nTo get started, see the usage examples in the documentation:")
    print("  - Basic usage: doc/usage.md")
    print("  - Interactive simulation: deployment/simulation/README.md")

if __name__ == "__main__":
    main()