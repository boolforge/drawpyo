"""
Style parser module for drawio files.

This module provides functionality to parse and manipulate style strings
used in drawio files. Style strings are a fundamental part of the drawio
format, defining the visual appearance of shapes, connectors, and other
elements.

In drawio, styles are represented as semicolon-separated lists of key=value
pairs, with the first item optionally being a base style without an equals
sign. For example:
    "shape=rectangle;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;"

This module provides methods to:
- Parse style strings into dictionaries
- Create style strings from dictionaries
- Get specific values from style strings
- Set or modify values in style strings
- Remove values from style strings

These operations are essential for reading, modifying, and writing drawio
files with the correct visual appearance.

Technical details:
- Style strings can have a base style as the first item (without equals sign)
- Values can be strings, numbers, or booleans
- Numeric values are automatically converted to the appropriate type
- Boolean values ("true"/"false") are converted to Python booleans
"""


class StyleParser:
    """
    Class for parsing and manipulating drawio style strings.
    
    Drawio style strings are semicolon-separated lists of key=value pairs,
    with the first item optionally being a base style without an equals sign.
    This class provides methods to parse these strings, extract values, and
    create new style strings.
    
    All methods are static, so this class can be used without instantiation:
    
    Example:
        # Parse a style string to a dictionary
        style_str = "shape=rectangle;fillColor=#f5f5f5;strokeColor=#666666;"
        style_dict = StyleParser.parse_style(style_str)
        print(style_dict)  # {'shape': 'rectangle', 'fillColor': '#f5f5f5', 'strokeColor': '#666666'}
        
        # Create a style string from a dictionary
        new_style = StyleParser.create_style(style_dict)
        print(new_style)  # "shape=rectangle;fillColor=#f5f5f5;strokeColor=#666666"
        
        # Get a specific value
        color = StyleParser.get_style_value(style_str, 'fillColor')
        print(color)  # "#f5f5f5"
        
        # Set a specific value
        updated_style = StyleParser.set_style_value(style_str, 'fillColor', '#ff0000')
        print(updated_style)  # "shape=rectangle;fillColor=#ff0000;strokeColor=#666666"
    """
    
    @staticmethod
    def parse_style(style_str):
        """
        Parse a drawio style string into a dictionary.
        
        This method converts a semicolon-separated style string into a
        dictionary of key-value pairs. It handles special cases like:
        - Base style (first item without equals sign)
        - Numeric values (converted to int or float)
        - Boolean values (converted to True/False)
        
        Args:
            style_str (str): The style string to parse
            
        Returns:
            dict: A dictionary of style attributes and values
            
        Example:
            # Parse a simple style string
            style_dict = StyleParser.parse_style("shape=rectangle;fillColor=#f5f5f5;")
            print(style_dict)  # {'shape': 'rectangle', 'fillColor': '#f5f5f5'}
            
            # Parse a style string with a base style
            style_dict = StyleParser.parse_style("rounded;fillColor=#f5f5f5;")
            print(style_dict)  # {'baseStyle': 'rounded', 'fillColor': '#f5f5f5'}
            
            # Parse a style string with numeric and boolean values
            style_dict = StyleParser.parse_style("shape=rectangle;opacity=50;dashed=true;")
            print(style_dict)  # {'shape': 'rectangle', 'opacity': 50, 'dashed': True}
        """
        if not style_str:
            return {}
        
        style_dict = {}
        parts = style_str.split(';')
        
        for i, part in enumerate(parts):
            if not part:
                continue
                
            # First part might be a base style without an equals sign
            if i == 0 and '=' not in part:
                style_dict['baseStyle'] = part
            elif '=' in part:
                key, value = part.split('=', 1)
                
                # Convert numeric values
                if value.isdigit():
                    # Integer value
                    value = int(value)
                elif value.replace('.', '', 1).isdigit() and value.count('.') == 1:
                    # Float value
                    value = float(value)
                # Convert boolean values
                elif value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                    
                style_dict[key] = value
        
        return style_dict
    
    @staticmethod
    def create_style(style_dict):
        """
        Create a drawio style string from a dictionary.
        
        This method converts a dictionary of style attributes and values
        into a semicolon-separated style string. It handles special cases like:
        - Base style (stored under the 'baseStyle' key)
        - None values (skipped)
        
        Args:
            style_dict (dict): A dictionary of style attributes and values
            
        Returns:
            str: A drawio style string
            
        Example:
            # Create a style string from a dictionary
            style_dict = {
                'shape': 'rectangle',
                'fillColor': '#f5f5f5',
                'strokeColor': '#666666'
            }
            style_str = StyleParser.create_style(style_dict)
            print(style_str)  # "shape=rectangle;fillColor=#f5f5f5;strokeColor=#666666"
            
            # Create a style string with a base style
            style_dict = {
                'baseStyle': 'rounded',
                'fillColor': '#f5f5f5'
            }
            style_str = StyleParser.create_style(style_dict)
            print(style_str)  # "rounded;fillColor=#f5f5f5"
        """
        if not style_dict:
            return ""
            
        style_parts = []
        
        # Handle base style first
        if 'baseStyle' in style_dict:
            style_parts.append(str(style_dict['baseStyle']))
            
        # Add all other key=value pairs
        for key, value in style_dict.items():
            if key != 'baseStyle' and value is not None:
                style_parts.append(f"{key}={value}")
                
        return ';'.join(style_parts)
    
    @staticmethod
    def get_style_value(style_str, key, default=None):
        """
        Get a specific value from a style string.
        
        This method parses a style string and extracts the value for a
        specific key. If the key is not found, it returns the default value.
        
        Args:
            style_str (str): The style string to parse
            key (str): The key to look for
            default: The default value to return if the key is not found
            
        Returns:
            The value for the key, or the default if not found
            
        Example:
            # Get a value from a style string
            style_str = "shape=rectangle;fillColor=#f5f5f5;strokeColor=#666666;"
            
            color = StyleParser.get_style_value(style_str, 'fillColor')
            print(color)  # "#f5f5f5"
            
            # Get a value with a default
            width = StyleParser.get_style_value(style_str, 'strokeWidth', 1)
            print(width)  # 1 (default value)
        """
        style_dict = StyleParser.parse_style(style_str)
        return style_dict.get(key, default)
    
    @staticmethod
    def set_style_value(style_str, key, value):
        """
        Set a specific value in a style string.
        
        This method parses a style string, sets or updates a specific key-value
        pair, and returns the modified style string.
        
        Args:
            style_str (str): The style string to modify
            key (str): The key to set
            value: The value to set
            
        Returns:
            str: The modified style string
            
        Example:
            # Set a value in a style string
            style_str = "shape=rectangle;fillColor=#f5f5f5;strokeColor=#666666;"
            
            # Change an existing value
            updated_style = StyleParser.set_style_value(style_str, 'fillColor', '#ff0000')
            print(updated_style)  # "shape=rectangle;fillColor=#ff0000;strokeColor=#666666"
            
            # Add a new value
            updated_style = StyleParser.set_style_value(style_str, 'dashed', True)
            print(updated_style)  # "shape=rectangle;fillColor=#f5f5f5;strokeColor=#666666;dashed=true"
        """
        style_dict = StyleParser.parse_style(style_str)
        style_dict[key] = value
        return StyleParser.create_style(style_dict)
    
    @staticmethod
    def remove_style_value(style_str, key):
        """
        Remove a specific key-value pair from a style string.
        
        This method parses a style string, removes a specific key-value
        pair if it exists, and returns the modified style string.
        
        Args:
            style_str (str): The style string to modify
            key (str): The key to remove
            
        Returns:
            str: The modified style string
            
        Example:
            # Remove a value from a style string
            style_str = "shape=rectangle;fillColor=#f5f5f5;strokeColor=#666666;"
            
            updated_style = StyleParser.remove_style_value(style_str, 'fillColor')
            print(updated_style)  # "shape=rectangle;strokeColor=#666666"
            
            # Remove a non-existent key (no change)
            updated_style = StyleParser.remove_style_value(style_str, 'dashed')
            print(updated_style)  # "shape=rectangle;fillColor=#f5f5f5;strokeColor=#666666"
        """
        style_dict = StyleParser.parse_style(style_str)
        if key in style_dict:
            del style_dict[key]
        return StyleParser.create_style(style_dict)
