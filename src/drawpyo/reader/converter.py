"""
Converter module for drawio files.

This module provides functionality to convert between drawio XML elements
and drawpyo objects. It serves as a bridge between the XML representation
of drawio diagrams and the object-oriented model used by drawpyo.

The converter handles the transformation of:
- mxGraphModel elements to drawpyo File and Page objects
- mxCell elements to drawpyo Object and Edge instances
- mxGeometry elements to position and size information
- Style strings to object properties

This module is a critical component in the process of reading existing
drawio files and making them available for manipulation through the
drawpyo API.

Technical details:
- Uses a two-pass approach: first creating all objects, then setting relationships
- Maps cell IDs to drawpyo objects for reference resolution
- Handles both vertex (shape) and edge (connector) elements
- Applies styles from the drawio XML to drawpyo objects
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
    to drawpyo objects that can be manipulated programmatically. It handles
    the conversion of the entire file structure, including pages, shapes,
    and connectors.
    
    The conversion process involves:
    1. Creating a drawpyo File object
    2. Converting each diagram to a Page
    3. Converting each mxCell to an Object or Edge
    4. Setting parent-child relationships and connecting edges
    
    Example:
        parser = DrawioParser()
        converter = XmlToPythonConverter()
        
        # Parse a drawio file
        parsed_data = parser.parse_file("example.drawio")
        
        # Convert the parsed data to drawpyo objects
        file = converter.convert_file(parsed_data)
        
        # Access the converted objects
        for page in file.pages:
            print(f"Page: {page.name}")
            for obj in page.objects:
                print(f"  Object: {obj}")
    """
    
    def __init__(self):
        """
        Initialize the converter.
        
        Creates a new XmlToPythonConverter instance with an empty mapping
        of cell IDs to drawpyo objects.
        
        The id_to_object dictionary is used during the conversion process
        to keep track of created objects and establish relationships between
        them.
        
        Example:
            converter = XmlToPythonConverter()
        """
        self.id_to_object = {}  # Maps cell IDs to drawpyo objects
    
    def convert_file(self, parsed_data):
        """
        Convert parsed drawio file data to a drawpyo File object.
        
        This method takes the parsed data from a DrawioParser and converts
        it to a drawpyo File object containing Pages, Objects, and Edges.
        
        Args:
            parsed_data (dict): Parsed drawio file data from DrawioParser
                with the structure:
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
                            'content': Element
                        },
                        ...
                    ]
                }
            
        Returns:
            File: A drawpyo File object containing the converted diagrams
            
        Example:
            # Parse a drawio file
            parsed_data = parser.parse_file("example.drawio")
            
            # Convert the parsed data to a drawpyo File
            file = converter.convert_file(parsed_data)
            
            # Save the converted file
            file.write(file_path="/path/to/output", file_name="converted.drawio")
        """
        file_info = parsed_data['file_info']
        
        # Create a new drawpyo File
        file = File()
        
        # Set file attributes from the parsed data
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
        
        This method takes a single diagram from the parsed data and converts
        it to a drawpyo Page object containing Objects and Edges.
        
        Args:
            diagram_data (dict): Parsed diagram data from DrawioParser
                with the structure:
                {
                    'id': str,
                    'name': str,
                    'content': Element  # XML Element representing the mxGraphModel
                }
            
        Returns:
            Page: A drawpyo Page object containing the converted elements
            
        Example:
            # Convert a single diagram to a Page
            page = converter.convert_diagram(parsed_data['diagrams'][0])
            
            # Access the objects in the page
            for obj in page.objects:
                print(f"Object: {obj}")
        """
        # Create a new drawpyo Page with the diagram name
        page = Page(diagram_data['name'])
        
        # Reset the ID to object mapping for this diagram
        # This ensures that IDs from different diagrams don't conflict
        self.id_to_object = {}
        
        # Get the mxGraphModel element (root of the diagram content)
        graph_model = diagram_data['content']
        
        # Get the root element containing all cells
        root = graph_model.find('root')
        if root is None:
            # If there's no root element, return an empty page
            return page
        
        # First pass: create all objects
        # This creates all Objects and Edges but doesn't set relationships yet
        for cell in root.findall('mxCell'):
            self._create_object_from_cell(cell, page)
        
        # Second pass: set parent-child relationships and connect edges
        # This sets the parent-child hierarchy and connects edges to their sources and targets
        for cell in root.findall('mxCell'):
            self._set_relationships(cell)
        
        return page
    
    def _create_object_from_cell(self, cell, page):
        """
        Create a drawpyo object from an mxCell element.
        
        This method examines an mxCell element and creates the appropriate
        drawpyo object (Object or Edge) based on its attributes.
        
        Args:
            cell (Element): An mxCell XML element
            page (Page): The drawpyo Page to add the object to
            
        Returns:
            Object or Edge: The created drawpyo object, or None for special cells
            
        Note:
            This method is part of the first pass of the conversion process.
            It creates objects but doesn't set relationships between them.
        """
        cell_id = cell.get('id')
        
        # Skip the root cells (0 and 1)
        # Cell 0 is the diagram root, Cell 1 is the default parent
        if cell_id in ('0', '1'):
            return None
        
        # Check if it's an edge or a vertex
        is_edge = cell.get('edge') == '1'
        is_vertex = cell.get('vertex') == '1'
        
        if is_edge:
            # Create an edge (connector)
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
        
        This method converts an mxCell element with vertex="1" to a drawpyo
        Object, setting its properties based on the cell's attributes and
        geometry.
        
        Args:
            cell (Element): An mxCell XML element with vertex="1"
            page (Page): The drawpyo Page to add the object to
            
        Returns:
            Object: The created drawpyo Object
            
        Note:
            This method handles the conversion of shapes (rectangles, ellipses, etc.)
            and sets their position, size, and style properties.
        """
        # Get basic attributes
        cell_id = cell.get('id')
        value = cell.get('value', '')
        style = cell.get('style', '')
        
        # Create a basic object with the cell's value as its text
        obj = Object(value=value)
        obj.page = page
        
        # Apply style if present
        # This sets properties like fillColor, strokeColor, etc.
        if style:
            obj.apply_style_string(style)
        
        # Set geometry if present
        geometry = cell.find('mxGeometry')
        if geometry is not None:
            # Extract position and size from the geometry element
            x = float(geometry.get('x', 0))
            y = float(geometry.get('y', 0))
            width = float(geometry.get('width', 120))
            height = float(geometry.get('height', 60))
            
            # Set position and size on the object
            obj.position = (x, y)
            obj.width = width
            obj.height = height
        
        return obj
    
    def _create_edge_from_cell(self, cell, page):
        """
        Create a drawpyo Edge from an mxCell edge element.
        
        This method converts an mxCell element with edge="1" to a drawpyo
        Edge, setting its properties based on the cell's attributes.
        
        Args:
            cell (Element): An mxCell XML element with edge="1"
            page (Page): The drawpyo Page to add the edge to
            
        Returns:
            Edge: The created drawpyo Edge
            
        Note:
            This method handles the conversion of connectors (lines, arrows, etc.)
            but doesn't set their source and target objects yet. That happens in
            the second pass during _set_relationships.
        """
        # Get basic attributes
        value = cell.get('value', '')
        style = cell.get('style', '')
        
        # Create a basic edge with the cell's value as its label
        edge = Edge(label=value)
        edge.page = page
        
        # Apply style if present
        # This sets properties like strokeColor, endArrow, etc.
        if style:
            edge.apply_style_string(style)
        
        # Source and target will be set in the second pass
        # during _set_relationships
        
        return edge
    
    def _set_relationships(self, cell):
        """
        Set parent-child relationships and connect edges.
        
        This method is part of the second pass of the conversion process.
        It sets parent-child relationships between objects and connects
        edges to their source and target objects.
        
        Args:
            cell (Element): An mxCell XML element
            
        Note:
            This method relies on the id_to_object dictionary populated
            during the first pass to resolve references between objects.
        """
        cell_id = cell.get('id')
        
        # Skip the root cells (0 and 1)
        if cell_id in ('0', '1'):
            return
        
        # Get the object corresponding to this cell
        obj = self.id_to_object.get(cell_id)
        if obj is None:
            # If the object wasn't created in the first pass, skip it
            return
        
        # Set parent relationship
        parent_id = cell.get('parent')
        if parent_id and parent_id not in ('0', '1'):
            # If the parent is not the root or default parent,
            # set the parent-child relationship
            parent_obj = self.id_to_object.get(parent_id)
            if parent_obj:
                obj.parent = parent_obj
        
        # If it's an edge, set source and target
        if isinstance(obj, Edge):
            source_id = cell.get('source')
            target_id = cell.get('target')
            
            # Set the source object if specified
            if source_id:
                source_obj = self.id_to_object.get(source_id)
                if source_obj:
                    obj.source = source_obj
            
            # Set the target object if specified
            if target_id:
                target_obj = self.id_to_object.get(target_id)
                if target_obj:
                    obj.target = target_obj
