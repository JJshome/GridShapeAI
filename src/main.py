#!/usr/bin/env python
# GridShapeAI command-line interface

import argparse
import sys
import os
import torch
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from shape_generator.shape_generator import ShapeGenerator
from renderer.renderer import Renderer
from renderer.renderer_3d import Renderer3D
from utils.file_utils import FileUtils

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='GridShapeAI - Generate precise geometric shapes from text prompts')
    
    # Main command argument
    parser.add_argument('command', choices=['generate', 'render', 'export', 'info'],
                        help='Command to execute')
    
    # Input arguments
    parser.add_argument('--prompt', '-p', type=str,
                        help='Text prompt describing the shape to generate')
    parser.add_argument('--input', '-i', type=str,
                        help='Input file for shape data (.npy format)')
    
    # Output arguments
    parser.add_argument('--output', '-o', type=str,
                        help='Output file path')
    parser.add_argument('--format', '-f', type=str, 
                        choices=['png', 'svg', 'obj', 'stl', 'npy'],
                        default='png',
                        help='Output file format')
    
    # Rendering options
    parser.add_argument('--view', '-v', type=str,
                        choices=['projections', 'isometric', 'slice-xy', 'slice-xz', 'slice-yz'],
                        default='projections',
                        help='View type for rendering')
    parser.add_argument('--colormap', '-c', type=str,
                        default='viridis',
                        help='Colormap for visualization')
    parser.add_argument('--slice-idx', type=int,
                        help='Index for slice views')
    
    # Model options
    parser.add_argument('--model-path', type=str,
                        help='Path to a trained model checkpoint')
    parser.add_argument('--use-direct', action='store_true',
                        help='Use direct shape creation instead of neural network')
    parser.add_argument('--grid-size', type=int, default=100,
                        help='Size of the grid (default: 100)')
    
    # Device options
    parser.add_argument('--device', type=str, choices=['cpu', 'cuda'], 
                        default='cuda' if torch.cuda.is_available() else 'cpu',
                        help='Device to run the model on')
    
    return parser.parse_args()

def generate_shape(args):
    """Generate a shape from a text prompt."""
    if not args.prompt:
        print("Error: --prompt is required for generate command")
        sys.exit(1)
    
    print(f"Generating shape from prompt: {args.prompt}")
    
    # Initialize generator
    generator = ShapeGenerator(
        model_path=args.model_path, 
        device=args.device,
        grid_size=args.grid_size
    )
    
    # Generate shape
    shape = generator.generate(args.prompt, use_direct=args.use_direct)
    
    # Save shape if output specified
    if args.output:
        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save shape data as numpy file
        if args.format == 'npy':
            FileUtils.save_grid_numpy(shape.grid, args.output)
            print(f"Shape data saved to {args.output}")
        else:
            # Save visualization
            render_shape(shape, args)
    else:
        # If no output specified, just render
        render_shape(shape, args)
    
    return shape

def render_shape(shape, args):
    """Render a shape according to options."""
    if isinstance(shape, str):
        # Load shape from file
        grid = FileUtils.load_grid_numpy(shape, device=args.device)
    else:
        # Use provided shape object
        grid = shape.grid
    
    # Initialize renderers
    renderer = Renderer()
    renderer_3d = Renderer3D()
    
    # Set output filename
    if args.output:
        output_filename = args.output
    else:
        output_filename = 'shape_output.' + args.format
    
    # Render based on view type
    if args.view == 'projections':
        fig = renderer.render_projection(grid, projection_type='max', colormap=args.colormap)
    elif args.view == 'isometric':
        fig = renderer.render_isometric(grid, colormap=args.colormap)
    elif args.view.startswith('slice-'):
        axis = {'slice-xy': 2, 'slice-xz': 1, 'slice-yz': 0}[args.view]
        slice_idx = args.slice_idx if args.slice_idx is not None else grid.size // 2
        fig = renderer.render_slice(grid, axis, slice_idx, colormap=args.colormap)
    
    # Save or display the figure
    if args.output:
        renderer.save_image(fig, output_filename)
        print(f"Visualization saved to {output_filename}")
    else:
        plt.show()

def export_shape(args):
    """Export a shape to various formats."""
    if not args.input:
        print("Error: --input is required for export command")
        sys.exit(1)
    
    if not args.output:
        print("Error: --output is required for export command")
        sys.exit(1)
    
    print(f"Exporting shape from {args.input} to {args.output}")
    
    # Load shape
    grid = FileUtils.load_grid_numpy(args.input, device=args.device)
    
    # Initialize renderers
    renderer = Renderer()
    renderer_3d = Renderer3D()
    
    # Export based on format
    if args.format == 'png':
        fig = renderer.render_projection(grid, colormap=args.colormap)
        renderer.save_image(fig, args.output)
    elif args.format == 'svg':
        # SVG exporting would go here
        # For now, we'll just create a PNG
        fig = renderer.render_projection(grid, colormap=args.colormap)
        renderer.save_image(fig, args.output.replace('.svg', '.png'))
        print("Note: Direct SVG export not implemented. Saved as PNG instead.")
    elif args.format in ['obj', 'stl']:
        # Generate mesh
        mesh = renderer_3d.generate_mesh(grid, threshold=0.5)
        
        # Export mesh to appropriate format
        if args.format == 'obj':
            renderer_3d.export_obj(mesh, args.output)
        else:  # STL
            renderer_3d.export_stl(mesh, args.output)
    
    print(f"Shape exported to {args.output}")

def show_info(args):
    """Show information about a shape file."""
    if not args.input:
        print("Error: --input is required for info command")
        sys.exit(1)
    
    print(f"Showing information for shape in {args.input}")
    
    # Load shape
    grid = FileUtils.load_grid_numpy(args.input, device=args.device)
    
    # Get basic information
    active_points = grid.count_active_points()
    total_points = grid.size ** 3
    density = active_points / total_points * 100
    
    # Print information
    print(f"Grid size: {grid.size}x{grid.size}x{grid.size}")
    print(f"Total points: {total_points}")
    print(f"Active points: {active_points} ({density:.2f}%)")
    
    # Get axis projections
    xy_max = torch.max(grid.data, dim=2)[0].max().item()
    xz_max = torch.max(grid.data, dim=1)[0].max().item()
    yz_max = torch.max(grid.data, dim=0)[0].max().item()
    
    print(f"Maximum values - XY: {xy_max:.4f}, XZ: {xz_max:.4f}, YZ: {yz_max:.4f}")
    
    # Visualize shape
    renderer = Renderer()
    fig = renderer.render_projection(grid, colormap=args.colormap)
    plt.show()

def main():
    """Main function."""
    args = parse_args()
    
    # Execute the requested command
    if args.command == 'generate':
        generate_shape(args)
    elif args.command == 'render':
        if not args.input:
            print("Error: --input is required for render command")
            sys.exit(1)
        render_shape(args.input, args)
    elif args.command == 'export':
        export_shape(args)
    elif args.command == 'info':
        show_info(args)

if __name__ == "__main__":
    main()