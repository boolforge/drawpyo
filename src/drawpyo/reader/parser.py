"""
Parser module for drawio files.

This module provides functionality to parse drawio XML files and extract
the diagram content. It handles both uncompressed XML and compressed content
that is encoded in base64+deflate format.

The drawio file format consists of an XML structure with a root <mxfile> element
containing one or more <diagram> elements. Each diagram represents a page in the
drawio editor. The content of each diagram can be either direct XML or compressed
data that needs to be decompressed before parsing.

This module works closely with the DrawioDecompressor to handle compressed content
and provides a structured representation of the drawio file that can be used by
the XmlToPythonConverter to create drawpyo objects.

Technical details:
- The parser uses xml.etree.ElementTree for XML parsing
- It extracts file metadata (host, version, etc.) from the mxfile element
- It handles multiple diagrams (pages) in a single file
- It automatically detects and decompresses compressed content
"""

import xml.etree.ElementTree as ET
from .decompressor import DrawioDecompressor


class DrawioParser:
    """
    Class for parsing drawio XML files.
    
    Drawio files are XML files with a specific structure. This class provides
    methods to parse these files and extract the diagram content, handling both
    direct XML content and compressed content.
    
    The parser extracts the following information:
    - File metadata (host, modified date, agent, version, type)
    - Diagram information (id, name)
    - Diagram content (mxGraphModel element)
    
    Example:
        parser = DrawioParser()
        parsed_data = parser.parse_file("example.drawio")
        
        # Access file information
        file_info = parsed_data['file_info']
        print(f"File created with: {file_info['host']}")
        
        # Access diagrams
        for diagram in parsed_data['diagrams']:
            print(f"Diagram: {diagram['name']}")
            # Process diagram content (XML Element)
            content = diagram['content']
    """
    
    def __init__(self):
        """
        Initialize the parser.
        
        Creates a new DrawioParser instance with a DrawioDecompressor for handling
        compressed content.
        
        Example:
            parser = DrawioParser()
        """
        self.decompressor = DrawioDecompressor()
    
    def parse_file(self, file_path):
        """
        Parse a drawio file and extract its content.
        
        This method reads a drawio file from disk, parses its XML structure,
        and extracts the file information and diagram content. If the diagram
        content is compressed, it will be decompressed automatically.
        
        Args:
            file_path (str): Path to the drawio file
            
        Returns:
            dict: A dictionary containing the parsed content with the following structure:
                {
                    'file_info': {
                        'host': str,       # Application that created the file
                        'modified': str,    # Last modification date
                        'agent': str,       # User agent information
                        'version': str,     # Format version
                        'type': str         # File type
                    },
                    'diagrams': [
                        {
                            'id': str,      # Diagram identifier
                            'name': str,    # Diagram name
                            'content': Element  # XML Element representing the mxGraphModel
                        },
                        ...
                    ]
                }
                
        Raises:
            ValueError: If the file cannot be parsed or is not a valid drawio file
            
        Example:
            try:
                parsed_data = parser.parse_file("example.drawio")
                
                # Print file information
                print(f"File created with: {parsed_data['file_info']['host']}")
                print(f"Last modified: {parsed_data['file_info']['modified']}")
                
                # Print diagram information
                for diagram in parsed_data['diagrams']:
                    print(f"Diagram: {diagram['name']} (ID: {diagram['id']})")
                    
            except ValueError as e:
                print(f"Error parsing file: {e}")
        """
        try:
            # Parse the XML file
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Verify that it's a drawio file
            if root.tag != 'mxfile':
                raise ValueError("Not a valid drawio file: root element is not 'mxfile'")
            
            # Extract file information from the root element
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
                # Get diagram attributes
                diagram_id = diagram_elem.get('id', '')
                diagram_name = diagram_elem.get('name', '')
                
                # Get diagram content (may be compressed)
                content = diagram_elem.text.strip() if diagram_elem.text else ''
                
                # Check if content is compressed and decompress if necessary
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
                
                # Add the diagram to the list
                diagrams.append({
                    'id': diagram_id,
                    'name': diagram_name,
                    'content': content_root
                })
            
            # Return the parsed data
            return {
                'file_info': file_info,
                'diagrams': diagrams
            }
            
        except ET.ParseError as e:
            # Handle XML parsing errors
            raise ValueError(f"Failed to parse file as XML: {str(e)}")
        except Exception as e:
            # Handle other errors
            raise ValueError(f"Failed to parse drawio file: {str(e)}")
    
    def parse_xml_string(self, xml_string):
        """
        Parse a drawio XML string and extract its content.
        
        This method is similar to parse_file, but it takes an XML string
        instead of a file path. This is useful when the XML is obtained
        from a source other than a file, such as a network request.
        
        Args:
            xml_string (str): The drawio XML string
            
        Returns:
            dict: A dictionary containing the parsed content (same structure as parse_file)
                
        Raises:
            ValueError: If the string cannot be parsed or is not a valid drawio XML
            
        Example:
            xml_string = '''
            <mxfile host="app.diagrams.net" modified="2023-01-01T12:00:00.000Z">
                <diagram id="abc123" name="Page-1">
                    <mxGraphModel>...</mxGraphModel>
                </diagram>
            </mxfile>
            '''
            
            try:
                parsed_data = parser.parse_xml_string(xml_string)
                # Process the parsed data
            except ValueError as e:
                print(f"Error parsing XML: {e}")
        """
        try:
            # Parse the XML string
            root = ET.fromstring(xml_string)
            
            # Verify that it's a drawio file
            if root.tag != 'mxfile':
                raise ValueError("Not a valid drawio XML: root element is not 'mxfile'")
            
            # Extract file information from the root element
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
                # Get diagram attributes
                diagram_id = diagram_elem.get('id', '')
                diagram_name = diagram_elem.get('name', '')
                
                # Get diagram content (may be compressed)
                content = diagram_elem.text.strip() if diagram_elem.text else ''
                
                # Check if content is compressed and decompress if necessary
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
                
                # Add the diagram to the list
                diagrams.append({
                    'id': diagram_id,
                    'name': diagram_name,
                    'content': content_root
                })
            
            # Return the parsed data
            return {
                'file_info': file_info,
                'diagrams': diagrams
            }
            
        except ET.ParseError as e:
            # Handle XML parsing errors
            raise ValueError(f"Failed to parse string as XML: {str(e)}")
        except Exception as e:
            # Handle other errors
            raise ValueError(f"Failed to parse drawio XML string: {str(e)}")
