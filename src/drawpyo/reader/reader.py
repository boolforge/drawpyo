"""
Main reader module for drawio files.

This module provides the main interface for reading drawio files and
converting them to drawpyo objects.
"""

from .parser import DrawioParser
from .converter import XmlToPythonConverter


class DrawioReader:
    """
    Main class for reading drawio files and converting them to drawpyo objects.
    
    This class combines the parser and converter to provide a simple interface
    for reading drawio files and converting them to drawpyo objects that can
    be manipulated programmatically.
    """
    
    def __init__(self):
        """Initialize the reader with a parser and converter."""
        self.parser = DrawioParser()
        self.converter = XmlToPythonConverter()
    
    @classmethod
    def read_file(cls, file_path):
        """
        Read a drawio file and convert it to a drawpyo File object.
        
        This is the main method for reading drawio files. It parses the file
        and converts it to a drawpyo File object that can be manipulated
        programmatically.
        
        Args:
            file_path (str): Path to the drawio file
            
        Returns:
            File: A drawpyo File object containing the converted diagrams
            
        Raises:
            ValueError: If the file cannot be parsed or converted
        """
        reader = cls()
        parsed_data = reader.parser.parse_file(file_path)
        return reader.converter.convert_file(parsed_data)
    
    @classmethod
    def read_xml_string(cls, xml_string):
        """
        Read a drawio XML string and convert it to a drawpyo File object.
        
        Args:
            xml_string (str): The drawio XML string
            
        Returns:
            File: A drawpyo File object containing the converted diagrams
            
        Raises:
            ValueError: If the string cannot be parsed or converted
        """
        reader = cls()
        parsed_data = reader.parser.parse_xml_string(xml_string)
        return reader.converter.convert_file(parsed_data)
    
    def parse_and_convert(self, file_path):
        """
        Parse a drawio file and convert it to a drawpyo File object.
        
        This method is an instance-based alternative to the class methods.
        It uses the instance's parser and converter to read the file.
        
        Args:
            file_path (str): Path to the drawio file
            
        Returns:
            File: A drawpyo File object containing the converted diagrams
            
        Raises:
            ValueError: If the file cannot be parsed or converted
        """
        parsed_data = self.parser.parse_file(file_path)
        return self.converter.convert_file(parsed_data)
