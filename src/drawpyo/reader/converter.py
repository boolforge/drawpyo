"""
Converter module for drawio files.

This module provides functionality to convert between drawio XML elements
and drawpyo objects.
"""

import xml.etree.ElementTree as ET
from ..diagram.objects import Object, BasicObject
from ..diagram.edges import Edge, BasicEdge
from ..page import Page
from ..file import File


class XmlToPythonConverter:
    """
    Class for converting drawio XML elements to drawpyo objects.
    
    This class provides methods to convert XML elements from a drawio file
    to drawpyo objects that can be manipulated programmatically.
    """
    
    def __init__(self):
        """Initialize the converter."""
        self.id_to_object = {}  # Maps cell IDs to drawpyo objects
    
    def convert_file(self, parsed_data):
        """
        Convert parsed drawio file data to a drawpyo File object.
        
        Args:
            parsed_data (dict): Parsed drawio file data from DrawioParser
            
        Returns:
            File: A drawpyo File object containing the converted diagrams
        """
        file_info = parsed_data['file_info']
        
        # Create a new drawpyo File
        file = File()
        
        # Set file attributes
        file.host = file_info.get('host', 'Drawpyo')
        file.version = file_info.get('version', '21.6.5')
        file.type = file_info.get('type', 'device')
        
        # Convert each diagram to a Page
        for diagram_data in parsed_data['diagrams']:
            page = self.convert_diagram(diagram_data)
            file.add_page(page)
        
        return file
    
    def convert_diagram(self, diagram_data):
        """
        Convert a parsed diagram to a drawpyo Page object.
        
        Args:
            diagram_data (dict): Parsed diagram data from DrawioParser
            
        Returns:
            Page: A drawpyo Page object containing the converted elements
        """
        # Create a new drawpyo Page
        page = Page(diagram_data['name'])
        
        # Reset the ID to object mapping for this diagram
        self.id_to_object = {}
        
        # Get the mxGraphModel element
        graph_model = diagram_data['content']
        
        # Get the root element
        root = graph_model.find('root')
        if root is None:
            return page
        
        # First pass: create all objects
        for cell in root.findall('mxCell'):
            self._create_object_from_cell(cell, page)
        
        # Second pass: set parent-child relationships and connect edges
        for cell in root.findall('mxCell'):
            self._set_relationships(cell)
        
        return page
    
    def _create_object_from_cell(self, cell, page):
        """
        Create a drawpyo object from an mxCell element.
        
        Args:
            cell (Element): An mxCell XML element
            page (Page): The drawpyo Page to add the object to
            
        Returns:
            Object or Edge: The created drawpyo object
        """
        cell_id = cell.get('id')
        
        # Skip the root cells (0 and 1)
        if cell_id in ('0', '1'):
            return None
        
        # Check if it's an edge or a vertex
        is_edge = cell.get('edge') == '1'
        is_vertex = cell.get('vertex') == '1'
        
        if is_edge:
            # Create an edge
            edge = self._create_edge_from_cell(cell, page)
            self.id_to_object[cell_id] = edge
            return edge
        elif is_vertex:
            # Create a vertex (shape)
            obj = self._create_vertex_from_cell(cell, page)
            self.id_to_object[cell_id] = obj
            return obj
        else:
            # It might be a group or other special element
            # For now, create a basic object
            obj = BasicObject()
            obj.page = page
            self.id_to_object[cell_id] = obj
            return obj
    
    def _create_vertex_from_cell(self, cell, page):
        """
        Create a drawpyo Object from an mxCell vertex element.
        
        Args:
            cell (Element): An mxCell XML element with vertex="1"
            page (Page): The drawpyo Page to add the object to
            
        Returns:
            Object: The created drawpyo Object
        """
        # Get basic attributes
        cell_id = cell.get('id')
        value = cell.get('value', '')
        style = cell.get('style', '')
        
        # Create a basic object
        obj = Object(value=value)
        obj.page = page
        
        # Apply style
        if style:
            obj.apply_style_string(style)
        
        # Set geometry if present
        geometry = cell.find('mxGeometry')
        if geometry is not None:
            x = float(geometry.get('x', 0))
            y = float(geometry.get('y', 0))
            width = float(geometry.get('width', 120))
            height = float(geometry.get('height', 60))
            
            obj.position = (x, y)
            obj.width = width
            obj.height = height
        
        return obj
    
    def _create_edge_from_cell(self, cell, page):
        """
        Create a drawpyo Edge from an mxCell edge element.
        
        Args:
            cell (Element): An mxCell XML element with edge="1"
            page (Page): The drawpyo Page to add the edge to
            
        Returns:
            Edge: The created drawpyo Edge
        """
        # Get basic attributes
        value = cell.get('value', '')
        style = cell.get('style', '')
        
        # Create a basic edge
        edge = Edge(label=value)
        edge.page = page
        
        # Apply style
        if style:
            edge.apply_style_string(style)
        
        # Source and target will be set in the second pass
        
        return edge
    
    def _set_relationships(self, cell):
        """
        Set parent-child relationships and connect edges.
        
        Args:
            cell (Element): An mxCell XML element
        """
        cell_id = cell.get('id')
        
        # Skip the root cells (0 and 1)
        if cell_id in ('0', '1'):
            return
        
        # Get the object corresponding to this cell
        obj = self.id_to_object.get(cell_id)
        if obj is None:
            return
        
        # Set parent relationship
        parent_id = cell.get('parent')
        if parent_id and parent_id not in ('0', '1'):
            parent_obj = self.id_to_object.get(parent_id)
            if parent_obj:
                obj.parent = parent_obj
        
        # If it's an edge, set source and target
        if isinstance(obj, Edge):
            source_id = cell.get('source')
            target_id = cell.get('target')
            
            if source_id:
                source_obj = self.id_to_object.get(source_id)
                if source_obj:
                    obj.source = source_obj
            
            if target_id:
                target_obj = self.id_to_object.get(target_id)
                if target_obj:
                    obj.target = target_obj
