"""
Main reader module for drawio files.

This module provides the main interface for reading drawio files and
converting them to drawpyo objects. It serves as the primary entry point
for users who want to read existing drawio files and work with them using
the drawpyo API.

The DrawioReader class combines the functionality of the parser and converter
to provide a simple, high-level interface for reading drawio files. It handles
the entire process of:
1. Reading the file from disk
2. Parsing the XML structure
3. Decompressing compressed content
4. Converting XML elements to drawpyo objects

This module is designed to be easy to use, with class methods that provide
a convenient interface for common operations.

Technical details:
- Uses DrawioParser to parse the file and extract diagram content
- Uses XmlToPythonConverter to convert XML elements to drawpyo objects
- Provides both class methods and instance methods for flexibility
- Handles both file paths and XML strings as input
"""

from .parser import DrawioParser
from .converter import XmlToPythonConverter


class DrawioReader:
    """
    Main class for reading drawio files and converting them to drawpyo objects.
    
    This class combines the parser and converter to provide a simple interface
    for reading drawio files and converting them to drawpyo objects that can
    be manipulated programmatically.
    
    The class provides both class methods for simple one-off operations and
    instance methods for more complex scenarios where you might want to reuse
    the parser and converter.
    
    Example using class methods:
        # Read a drawio file and convert it to a drawpyo File object
        file = DrawioReader.read_file("example.drawio")
        
        # Access the pages and objects in the file
        for page in file.pages:
            print(f"Page: {page.name}")
            for obj in page.objects:
                print(f"  Object: {obj}")
                
    Example using instance methods:
        # Create a reader instance
        reader = DrawioReader()
        
        # Parse and convert multiple files
        file1 = reader.parse_and_convert("example1.drawio")
        file2 = reader.parse_and_convert("example2.drawio")
    """
    
    def __init__(self):
        """
        Initialize the reader with a parser and converter.
        
        Creates a new DrawioReader instance with its own DrawioParser and
        XmlToPythonConverter instances. This is useful when you want to
        read multiple files and reuse the same parser and converter.
        
        Example:
            reader = DrawioReader()
            file1 = reader.parse_and_convert("example1.drawio")
            file2 = reader.parse_and_convert("example2.drawio")
        """
        self.parser = DrawioParser()
        self.converter = XmlToPythonConverter()
    
    @classmethod
    def read_file(cls, file_path):
        """
        Read a drawio file and convert it to a drawpyo File object.
        
        This is the main method for reading drawio files. It parses the file
        and converts it to a drawpyo File object that can be manipulated
        programmatically.
        
        This class method creates a temporary DrawioReader instance, uses it
        to read the file, and then discards it. This is convenient for one-off
        operations.
        
        Args:
            file_path (str): Path to the drawio file
            
        Returns:
            File: A drawpyo File object containing the converted diagrams
            
        Raises:
            ValueError: If the file cannot be parsed or converted
            
        Example:
            try:
                # Read a drawio file
                file = DrawioReader.read_file("example.drawio")
                
                # Access the pages in the file
                for page in file.pages:
                    print(f"Page: {page.name}")
                    
                # Save the file with modifications
                file.write(file_path="/path/to/output", file_name="modified.drawio")
                
            except ValueError as e:
                print(f"Error reading file: {e}")
        """
        reader = cls()
        parsed_data = reader.parser.parse_file(file_path)
        return reader.converter.convert_file(parsed_data)
    
    @classmethod
    def read_xml_string(cls, xml_string):
        """
        Read a drawio XML string and convert it to a drawpyo File object.
        
        This method is similar to read_file, but it takes an XML string
        instead of a file path. This is useful when the XML is obtained
        from a source other than a file, such as a network request or
        a database.
        
        Args:
            xml_string (str): The drawio XML string
            
        Returns:
            File: A drawpyo File object containing the converted diagrams
            
        Raises:
            ValueError: If the string cannot be parsed or converted
            
        Example:
            xml_string = '''
            <mxfile host="app.diagrams.net" modified="2023-01-01T12:00:00.000Z">
                <diagram id="abc123" name="Page-1">
                    <mxGraphModel>...</mxGraphModel>
                </diagram>
            </mxfile>
            '''
            
            try:
                # Parse the XML string
                file = DrawioReader.read_xml_string(xml_string)
                
                # Access the pages in the file
                for page in file.pages:
                    print(f"Page: {page.name}")
                    
            except ValueError as e:
                print(f"Error parsing XML: {e}")
        """
        reader = cls()
        parsed_data = reader.parser.parse_xml_string(xml_string)
        return reader.converter.convert_file(parsed_data)
    
    def parse_and_convert(self, file_path):
        """
        Parse a drawio file and convert it to a drawpyo File object.
        
        This method is an instance-based alternative to the class methods.
        It uses the instance's parser and converter to read the file.
        
        This is useful when you want to read multiple files and reuse the
        same parser and converter instances, which can be more efficient
        than creating new instances for each file.
        
        Args:
            file_path (str): Path to the drawio file
            
        Returns:
            File: A drawpyo File object containing the converted diagrams
            
        Raises:
            ValueError: If the file cannot be parsed or converted
            
        Example:
            # Create a reader instance
            reader = DrawioReader()
            
            try:
                # Parse and convert multiple files
                file1 = reader.parse_and_convert("example1.drawio")
                file2 = reader.parse_and_convert("example2.drawio")
                
                # Compare the files
                print(f"File 1 has {len(file1.pages)} pages")
                print(f"File 2 has {len(file2.pages)} pages")
                
            except ValueError as e:
                print(f"Error reading file: {e}")
        """
        parsed_data = self.parser.parse_file(file_path)
        return self.converter.convert_file(parsed_data)
