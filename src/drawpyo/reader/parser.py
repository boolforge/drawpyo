"""
Parser module for drawio files.

This module provides functionality to parse drawio XML files and extract
the diagram content.
"""

import xml.etree.ElementTree as ET
from .decompressor import DrawioDecompressor


class DrawioParser:
    """
    Class for parsing drawio XML files.
    
    Drawio files are XML files with a specific structure. This class provides
    methods to parse these files and extract the diagram content.
    """
    
    def __init__(self):
        """Initialize the parser."""
        self.decompressor = DrawioDecompressor()
    
    def parse_file(self, file_path):
        """
        Parse a drawio file and extract its content.
        
        Args:
            file_path (str): Path to the drawio file
            
        Returns:
            dict: A dictionary containing the parsed content with the following structure:
                {
                    'file_info': {
                        'host': str,
                        'modified': str,
                        'agent': str,
                        'version': str,
                        'type': str
                    },
                    'diagrams': [
                        {
                            'id': str,
                            'name': str,
                            'content': Element  # XML Element representing the mxGraphModel
                        },
                        ...
                    ]
                }
                
        Raises:
            ValueError: If the file cannot be parsed or is not a valid drawio file
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            if root.tag != 'mxfile':
                raise ValueError("Not a valid drawio file: root element is not 'mxfile'")
            
            # Extract file information
            file_info = {
                'host': root.get('host', ''),
                'modified': root.get('modified', ''),
                'agent': root.get('agent', ''),
                'version': root.get('version', ''),
                'type': root.get('type', '')
            }
            
            # Extract diagrams
            diagrams = []
            for diagram_elem in root.findall('diagram'):
                diagram_id = diagram_elem.get('id', '')
                diagram_name = diagram_elem.get('name', '')
                
                # Get diagram content
                content = diagram_elem.text.strip() if diagram_elem.text else ''
                
                # Check if content is compressed
                if self.decompressor.is_compressed(content):
                    try:
                        content = self.decompressor.decompress(content)
                    except ValueError as e:
                        raise ValueError(f"Failed to decompress diagram '{diagram_name}': {str(e)}")
                
                # Parse the content as XML
                try:
                    content_root = ET.fromstring(content)
                except ET.ParseError as e:
                    raise ValueError(f"Failed to parse diagram content as XML: {str(e)}")
                
                diagrams.append({
                    'id': diagram_id,
                    'name': diagram_name,
                    'content': content_root
                })
            
            return {
                'file_info': file_info,
                'diagrams': diagrams
            }
            
        except ET.ParseError as e:
            raise ValueError(f"Failed to parse file as XML: {str(e)}")
        except Exception as e:
            raise ValueError(f"Failed to parse drawio file: {str(e)}")
    
    def parse_xml_string(self, xml_string):
        """
        Parse a drawio XML string and extract its content.
        
        Args:
            xml_string (str): The drawio XML string
            
        Returns:
            dict: A dictionary containing the parsed content (same structure as parse_file)
                
        Raises:
            ValueError: If the string cannot be parsed or is not a valid drawio XML
        """
        try:
            root = ET.fromstring(xml_string)
            
            if root.tag != 'mxfile':
                raise ValueError("Not a valid drawio XML: root element is not 'mxfile'")
            
            # Extract file information
            file_info = {
                'host': root.get('host', ''),
                'modified': root.get('modified', ''),
                'agent': root.get('agent', ''),
                'version': root.get('version', ''),
                'type': root.get('type', '')
            }
            
            # Extract diagrams
            diagrams = []
            for diagram_elem in root.findall('diagram'):
                diagram_id = diagram_elem.get('id', '')
                diagram_name = diagram_elem.get('name', '')
                
                # Get diagram content
                content = diagram_elem.text.strip() if diagram_elem.text else ''
                
                # Check if content is compressed
                if self.decompressor.is_compressed(content):
                    try:
                        content = self.decompressor.decompress(content)
                    except ValueError as e:
                        raise ValueError(f"Failed to decompress diagram '{diagram_name}': {str(e)}")
                
                # Parse the content as XML
                try:
                    content_root = ET.fromstring(content)
                except ET.ParseError as e:
                    raise ValueError(f"Failed to parse diagram content as XML: {str(e)}")
                
                diagrams.append({
                    'id': diagram_id,
                    'name': diagram_name,
                    'content': content_root
                })
            
            return {
                'file_info': file_info,
                'diagrams': diagrams
            }
            
        except ET.ParseError as e:
            raise ValueError(f"Failed to parse string as XML: {str(e)}")
        except Exception as e:
            raise ValueError(f"Failed to parse drawio XML string: {str(e)}")
