"""
Decompressor module for drawio files.

This module provides functionality to decompress content in drawio files
that is stored in base64+deflate format.
"""

import base64
import zlib


class DrawioDecompressor:
    """
    Class for handling compressed content in drawio files.
    
    Drawio files often contain diagram content that is compressed using
    base64 encoding and deflate compression. This class provides methods
    to decompress such content.
    """
    
    @staticmethod
    def is_compressed(content):
        """
        Check if the content appears to be compressed.
        
        Args:
            content (str): The content to check
            
        Returns:
            bool: True if the content appears to be base64 encoded, False otherwise
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
        
        Args:
            content (str): The compressed content
            
        Returns:
            str: The decompressed content as a UTF-8 string
            
        Raises:
            ValueError: If the content cannot be decompressed
        """
        try:
            # Decode base64
            decoded = base64.b64decode(content)
            
            # Decompress with zlib (deflate)
            # -zlib.MAX_WBITS tells zlib that there is no zlib header
            decompressed = zlib.decompress(decoded, -zlib.MAX_WBITS)
            
            # Convert to string
            return decompressed.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Failed to decompress content: {str(e)}")
    
    @staticmethod
    def compress(content):
        """
        Compress content using deflate and encode with base64.
        
        Args:
            content (str): The content to compress
            
        Returns:
            str: The compressed content as a base64 string
            
        Raises:
            ValueError: If the content cannot be compressed
        """
        try:
            # Convert to bytes if it's a string
            if isinstance(content, str):
                content = content.encode('utf-8')
            
            # Compress with zlib (deflate)
            # -zlib.MAX_WBITS tells zlib not to add a zlib header
            compressed = zlib.compress(content, 9)[2:-4]  # Remove zlib header and checksum
            
            # Encode as base64
            encoded = base64.b64encode(compressed)
            
            # Convert to string
            return encoded.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Failed to compress content: {str(e)}")
