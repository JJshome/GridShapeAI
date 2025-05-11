import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class TextProcessor:
    """Text processing utilities for shape generation.
    
    This class handles text prompt parsing, parameter extraction, and
    natural language processing for the GridShapeAI system.
    """
    
    def __init__(self):
        """Initialize the text processor.
        
        Downloads necessary NLTK resources if not already present.
        """
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
            
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        self.stop_words = set(stopwords.words('english'))
    
    def clean_text(self, text):
        """Clean and normalize text.
        
        Args:
            text: Input text string
            
        Returns:
            Cleaned text string
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep parentheses for coordinates
        text = re.sub(r'[^\w\s(),.-]', '', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_grid_size(self, text):
        """Extract grid size from text.
        
        Args:
            text: Input text string
            
        Returns:
            Dictionary with grid dimensions
        """
        grid_info = {}
        
        # Check for 3D grid
        match_3d = re.search(r'(\d+)\s*[xX]\s*(\d+)\s*[xX]\s*(\d+)', text)
        if match_3d:
            grid_info['dimensions'] = 3
            grid_info['size_x'] = int(match_3d.group(1))
            grid_info['size_y'] = int(match_3d.group(2))
            grid_info['size_z'] = int(match_3d.group(3))
            return grid_info
        
        # Check for 2D grid
        match_2d = re.search(r'(\d+)\s*[xX]\s*(\d+)\s*grid', text)
        if match_2d:
            grid_info['dimensions'] = 2
            grid_info['size_x'] = int(match_2d.group(1))
            grid_info['size_y'] = int(match_2d.group(2))
            grid_info['size_z'] = 1  # Default z dimension
            return grid_info
        
        # Default if no match
        grid_info['dimensions'] = 3
        grid_info['size_x'] = 100
        grid_info['size_y'] = 100
        grid_info['size_z'] = 100
        return grid_info
    
    def extract_coordinates(self, text):
        """Extract coordinates from text.
        
        Args:
            text: Input text string
            
        Returns:
            List of coordinate tuples
        """
        coordinates = []
        
        # Find all coordinate patterns like (x, y) or (x, y, z)
        coord_pattern = r'\(\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*(\d+))?\s*\)'
        matches = re.finditer(coord_pattern, text)
        
        for match in matches:
            if match.group(3):
                # 3D coordinate
                coord = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
            else:
                # 2D coordinate (default z=0)
                coord = (int(match.group(1)), int(match.group(2)), 0)
            
            coordinates.append(coord)
        
        return coordinates
    
    def extract_shape_type(self, text):
        """Extract shape type from text.
        
        Args:
            text: Input text string
            
        Returns:
            Shape type string
        """
        shape_types = {
            'square': ['square', 'squares'],
            'rectangle': ['rectangle', 'rectangles', 'rectangular'],
            'circle': ['circle', 'circles', 'circular'],
            'sphere': ['sphere', 'spheres', 'spherical'],
            'cube': ['cube', 'cubes', 'cubic'],
            'cylinder': ['cylinder', 'cylinders', 'cylindrical'],
            'cone': ['cone', 'cones', 'conical'],
            'torus': ['torus', 'toroid', 'toroidal', 'donut'],
            'pyramid': ['pyramid', 'pyramids', 'pyramidal'],
            'triangle': ['triangle', 'triangles', 'triangular'],
            'line': ['line', 'lines', 'segment', 'segments']
        }
        
        # Tokenize and clean text
        words = word_tokenize(self.clean_text(text))
        
        # Find shape type
        for shape_type, keywords in shape_types.items():
            if any(keyword in words for keyword in keywords):
                return shape_type
        
        # Default if no match
        return 'unknown'
    
    def extract_numeric_params(self, text):
        """Extract numeric parameters from text.
        
        Args:
            text: Input text string
            
        Returns:
            Dictionary of parameter names and values
        """
        params = {}
        
        # Common parameter patterns
        param_patterns = {
            'radius': r'radius\s+(\d+)',
            'diameter': r'diameter\s+(\d+)',
            'side_length': r'side\s+length\s+(\d+)|side\s+(\d+)',
            'width': r'width\s+(\d+)',
            'height': r'height\s+(\d+)',
            'depth': r'depth\s+(\d+)',
            'major_radius': r'major\s+radius\s+(\d+)',
            'minor_radius': r'minor\s+radius\s+(\d+)'
        }
        
        # Extract parameters
        for param_name, pattern in param_patterns.items():
            match = re.search(pattern, text)
            if match:
                # Some patterns have multiple groups, find the one that matched
                for i in range(1, len(match.groups()) + 1):
                    if match.group(i):
                        params[param_name] = int(match.group(i))
                        break
        
        # Derive additional parameters if needed
        if 'diameter' in params and 'radius' not in params:
            params['radius'] = params['diameter'] // 2
        
        return params
    
    def extract_boolean_operations(self, text):
        """Extract boolean operations from text.
        
        Args:
            text: Input text string
            
        Returns:
            List of operation dictionaries
        """
        operations = []
        
        # Boolean operation keywords
        union_keywords = ['union', 'unite', 'combine', 'add']
        intersection_keywords = ['intersection', 'intersect', 'common']
        difference_keywords = ['subtract', 'difference', 'remove', 'minus']
        
        # Tokenize and clean text
        words = word_tokenize(self.clean_text(text))
        
        # Find boolean operations in text
        for i, word in enumerate(words):
            if any(keyword in word for keyword in union_keywords):
                operations.append({'type': 'union', 'position': i})
            elif any(keyword in word for keyword in intersection_keywords):
                operations.append({'type': 'intersection', 'position': i})
            elif any(keyword in word for keyword in difference_keywords):
                operations.append({'type': 'difference', 'position': i})
        
        return operations
    
    def parse_prompt(self, text):
        """Parse a prompt to extract all shape parameters.
        
        Args:
            text: Input text string
            
        Returns:
            Dictionary with all extracted parameters
        """
        result = {}
        
        # Clean text for processing
        cleaned_text = self.clean_text(text)
        
        # Extract grid information
        result['grid'] = self.extract_grid_size(cleaned_text)
        
        # Extract shape type
        result['shape_type'] = self.extract_shape_type(cleaned_text)
        
        # Extract coordinates
        result['coordinates'] = self.extract_coordinates(cleaned_text)
        
        # Extract numeric parameters
        result['params'] = self.extract_numeric_params(cleaned_text)
        
        # Extract boolean operations
        result['operations'] = self.extract_boolean_operations(cleaned_text)
        
        return result