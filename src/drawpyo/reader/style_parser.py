"""
Style parser module for drawio files.

This module provides functionality to parse and manipulate style strings
used in drawio files.
"""


class StyleParser:
    """
    Class for parsing and manipulating drawio style strings.
    
    Drawio style strings are semicolon-separated lists of key=value pairs,
    with the first item optionally being a base style without an equals sign.
    This class provides methods to parse these strings, extract values, and
    create new style strings.
    """
    
    @staticmethod
    def parse_style(style_str):
        """
        Parse a drawio style string into a dictionary.
        
        Args:
            style_str (str): The style string to parse
            
        Returns:
            dict: A dictionary of style attributes and values
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
                    value = int(value)
                elif value.replace('.', '', 1).isdigit() and value.count('.') == 1:
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
        
        Args:
            style_dict (dict): A dictionary of style attributes and values
            
        Returns:
            str: A drawio style string
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
        
        Args:
            style_str (str): The style string to parse
            key (str): The key to look for
            default: The default value to return if the key is not found
            
        Returns:
            The value for the key, or the default if not found
        """
        style_dict = StyleParser.parse_style(style_str)
        return style_dict.get(key, default)
    
    @staticmethod
    def set_style_value(style_str, key, value):
        """
        Set a specific value in a style string.
        
        Args:
            style_str (str): The style string to modify
            key (str): The key to set
            value: The value to set
            
        Returns:
            str: The modified style string
        """
        style_dict = StyleParser.parse_style(style_str)
        style_dict[key] = value
        return StyleParser.create_style(style_dict)
    
    @staticmethod
    def remove_style_value(style_str, key):
        """
        Remove a specific key-value pair from a style string.
        
        Args:
            style_str (str): The style string to modify
            key (str): The key to remove
            
        Returns:
            str: The modified style string
        """
        style_dict = StyleParser.parse_style(style_str)
        if key in style_dict:
            del style_dict[key]
        return StyleParser.create_style(style_dict)
