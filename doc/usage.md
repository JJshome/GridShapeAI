# Usage Guide

## Basic Usage

```python
from gridshape_ai import ShapeGenerator

# Initialize the generator
generator = ShapeGenerator()

# Generate a shape from a text prompt
shape = generator.generate("100x100 grid, draw a square with corners at (20,20), (20,80), (80,80), and (80,20)")

# Visualize the shape
shape.visualize()

# Save the shape as an image
shape.save("square.png")

# Get the shape's coordinate data
coordinates = shape.get_coordinates()
print(coordinates)
```

## Advanced Usage

### 3D Shapes

```python
# Create a 3D shape
cube = generator.generate("100x100x100 grid, create a cube with side length 50 centered at (50,50,50)")

# Visualize in 3D
cube.visualize_3d()

# Export as a 3D model
cube.export_obj("cube.obj")
```

### Dynamic Parameters

```python
# Create a shape with parameters
circle_template = generator.create_template("100x100 grid, draw a circle with center at (50,50) and radius {radius}")

# Generate shapes with different parameters
circle1 = circle_template.generate({"radius": 20})
circle2 = circle_template.generate({"radius": 30})
```

### Reverse Mapping

```python
# Generate a shape
sphere = generator.generate("100x100x100 grid, create a sphere with radius 30 centered at (50,50,50)")

# Extract a mesh representation
mesh = sphere.to_mesh()

# Extract a point cloud
point_cloud = sphere.to_point_cloud()

# Get UV mapping
uv_map = sphere.get_uv_mapping()
```

## Batch Processing

```python
# Generate multiple shapes in batch
prompts = [
    "100x100 grid, draw a triangle with vertices at (20,20), (50,80), (80,20)",
    "100x100 grid, draw a circle with center at (50,50) and radius 30"
]

shapes = generator.generate_batch(prompts)

# Process all shapes
for i, shape in enumerate(shapes):
    shape.save(f"shape_{i}.png")
```

For more examples, see the `examples` directory.