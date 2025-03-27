"""
Reader module for drawpyo.

This module provides comprehensive functionality to read, parse, and convert existing drawio files
into drawpyo objects that can be manipulated programmatically. The module handles all aspects of
the drawio file format, including XML parsing, content decompression, style parsing, and conversion
to drawpyo objects.

The module consists of several components:
- DrawioDecompressor: Handles base64+deflate compressed content in drawio files
- DrawioParser: Parses drawio XML files and extracts diagram content
- StyleParser: Parses and manipulates drawio style strings
- XmlToPythonConverter: Converts drawio XML elements to drawpyo objects
- DrawioReader: Main interface for reading drawio files

Together, these components provide a complete solution for reading drawio files and converting
them to drawpyo objects that can be manipulated using the drawpyo API.

Example usage:
    from drawpyo.reader import DrawioReader
    
    # Read a drawio file and convert it to a drawpyo File object
    file = DrawioReader.read_file("example.drawio")
    
    # Access the pages and objects in the file
    for page in file.pages:
        print(f"Page: {page.name}")
        for obj in page.objects:
            print(f"  Object: {obj}")
"""

from .decompressor import DrawioDecompressor
from .parser import DrawioParser
from .converter import XmlToPythonConverter
from .reader import DrawioReader
from .style_parser import StyleParser

__all__ = [
    "DrawioDecompressor",
    "DrawioParser",
    "XmlToPythonConverter",
    "DrawioReader",
    "StyleParser",
]
