# GridShapeAI Simulation Environment

This interactive simulation allows you to experiment with the GridShapeAI system without writing code.

## Features

- Interactive text prompt input
- Real-time shape generation and visualization
- Parameter adjustment sliders
- 3D rotation and perspective controls
- Export options (PNG, SVG, OBJ, etc.)
- Embedded examples for learning

## Running the Simulation

```bash
cd deployment/simulation
python run_simulation.py
```

This will start a web server on http://localhost:8080 where you can access the simulation interface.

## Usage Examples

1. Basic 2D Shape: Enter "100x100 grid, draw a rectangle with corners at (20,20), (80,20), (80,60), (20,60)"
2. 3D Shape: Enter "100x100x100 grid, create a sphere with radius 30 centered at (50,50,50)"
3. Pattern: Enter "100x100 grid, create a 5x5 grid of circles with radius 5, spaced 15 units apart"
4. Complex Shape: Enter "100x100x100 grid, create a torus with major radius 30 and minor radius 10 centered at (50,50,50)"

Use the control panel on the right to adjust visualization options and export your creations.