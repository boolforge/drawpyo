"""
Decompressor module for drawio files.

This module provides functionality to decompress content in drawio files
that is stored in base64+deflate format.

In drawio files, diagram content is often compressed to reduce file size.
The compression method used is base64 encoding followed by deflate compression.
This module provides methods to detect, decompress, and compress such content.

Technical details:
- Base64 encoding: Converts binary data to ASCII text using 64 characters
- Deflate compression: Uses the zlib library without headers (raw deflate)
- The decompression process: base64 decode -> zlib decompress
- The compression process: zlib compress -> base64 encode

The DrawioDecompressor class provides static methods for these operations,
making it easy to use without instantiation.
"""

import base64
import zlib


class DrawioDecompressor:
    """
    Class for handling compressed content in drawio files.
    
    Drawio files often contain diagram content that is compressed using
    base64 encoding and deflate compression. This class provides methods
    to detect, decompress, and compress such content.
    
    All methods are static, so this class can be used without instantiation:
    
    Example:
        # Check if content is compressed
        is_compressed = DrawioDecompressor.is_compressed(content)
        
        # Decompress content
        if is_compressed:
            xml_content = DrawioDecompressor.decompress(content)
            
        # Compress content
        compressed = DrawioDecompressor.compress(xml_content)
    """
    
    @staticmethod
    def is_compressed(content):
        """
        Check if the content appears to be compressed.
        
        This method uses heuristics to determine if the content is likely
        to be base64 encoded. It checks for XML tags (which would indicate
        uncompressed content) and attempts to decode the content as base64.
        
        Args:
            content (str): The content to check
            
        Returns:
            bool: True if the content appears to be base64 encoded, False otherwise
            
        Example:
            # Check if diagram content is compressed
            if DrawioDecompressor.is_compressed(diagram_content):
                # Content is compressed, needs decompression
                decompressed = DrawioDecompressor.decompress(diagram_content)
            else:
                # Content is already in XML format
                xml_content = diagram_content
        """
        # Simple heuristic: if it contains XML tags, it's probably not compressed
        if "<" in content and ">" in content:
            return False
        
        # Try to decode as base64 to see if it's valid
        try:
            base64.b64decode(content)
            return True
        except:
            return False
    
    @staticmethod
    def decompress(content):
        """
        Decompress content that is encoded in base64 and compressed with deflate.
        
        This method performs the following steps:
        1. Decode the base64 encoded content to binary
        2. Decompress the binary data using zlib with raw deflate format
        3. Convert the decompressed binary data to a UTF-8 string
        
        Args:
            content (str): The compressed content (base64 encoded string)
            
        Returns:
            str: The decompressed content as a UTF-8 string
            
        Raises:
            ValueError: If the content cannot be decompressed
            
        Example:
            try:
                # Attempt to decompress diagram content
                xml_content = DrawioDecompressor.decompress(compressed_content)
                # Process the XML content
                root = ET.fromstring(xml_content)
            except ValueError as e:
                print(f"Error: {e}")
        """
        try:
            # Decode base64
            decoded = base64.b64decode(content)
            
            # Decompress with zlib (deflate)
            # -zlib.MAX_WBITS tells zlib that there is no zlib header
            # This is necessary for raw deflate data
            decompressed = zlib.decompress(decoded, -zlib.MAX_WBITS)
            
            # Convert to string
            return decompressed.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Failed to decompress content: {str(e)}")
    
    @staticmethod
    def compress(content):
        """
        Compress content using deflate and encode with base64.
        
        This method performs the following steps:
        1. Convert the content to bytes if it's a string
        2. Compress the bytes using zlib with raw deflate format
        3. Encode the compressed data as base64
        4. Convert the base64 bytes to a string
        
        Args:
            content (str or bytes): The content to compress
            
        Returns:
            str: The compressed content as a base64 string
            
        Raises:
            ValueError: If the content cannot be compressed
            
        Example:
            # Compress XML content for storage in a drawio file
            xml_content = '<mxGraphModel>...</mxGraphModel>'
            compressed = DrawioDecompressor.compress(xml_content)
            # Use compressed content in diagram element
            diagram_elem.text = compressed
        """
        try:
            # Convert to bytes if it's a string
            if isinstance(content, str):
                content = content.encode('utf-8')
            
            # Compress with zlib (deflate)
            # -zlib.MAX_WBITS tells zlib not to add a zlib header
            # This produces raw deflate data as used by drawio
            # The [2:-4] removes the zlib header and checksum
            compressed = zlib.compress(content, 9)[2:-4]
            
            # Encode as base64
            encoded = base64.b64encode(compressed)
            
            # Convert to string
            return encoded.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Failed to compress content: {str(e)}")
