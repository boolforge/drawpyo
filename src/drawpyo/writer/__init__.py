"""
Writer module for drawio files.

This module provides functionality to write drawpyo objects back to drawio XML files.
It handles the conversion from drawpyo objects to XML elements, compression of content,
and writing to disk in the proper drawio format.

The writer module completes the read-modify-write cycle for drawio files, allowing
users to:
1. Read existing drawio files using the reader module
2. Modify the content using the drawpyo API
3. Write the modified content back to drawio files using this writer module

This enables full programmatic control over drawio diagrams, making it possible
to create, modify, and save diagrams without using the drawio GUI.

Technical details:
- Converts drawpyo objects to mxGraphModel XML structure
- Handles compression of diagram content using base64+deflate
- Preserves file metadata and structure
- Supports multiple pages/diagrams in a single file
"""

import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import os
import uuid
from datetime import datetime
from ..diagram.objects import Object
from ..diagram.edges import Edge
from ..page import Page
from ..file import File
from ..reader.decompressor import DrawioDecompressor


class DrawioWriter:
    """
    Class for writing drawpyo objects to drawio files.
    
    This class provides methods to convert drawpyo objects (File, Page, Object, Edge)
    to drawio XML format and write them to disk. It handles the conversion process,
    including XML generation, content compression, and file writing.
    
    Example:
        # Create a writer
        writer = DrawioWriter()
        
        # Write a File object to disk
        writer.write_file(file, "output.drawio")
        
        # Get the XML content without writing to disk
        xml_content = writer.convert_file_to_xml(file)
    """
    
    def __init__(self, compress_content=True):
        """
        Initialize the writer with configuration options.
        
        Args:
            compress_content (bool): Whether to compress diagram content using base64+deflate.
                Default is True, which matches the behavior of the drawio application.
                
        Example:
            # Create a writer with default settings (compressed content)
            writer = DrawioWriter()
            
            # Create a writer that doesn't compress content (for debugging)
            writer = DrawioWriter(compress_content=False)
        """
        self.compress_content = compress_content
    
    def write_file(self, file, file_path):
        """
        Write a drawpyo File object to a drawio file.
        
        This method converts a drawpyo File object to drawio XML format and
        writes it to the specified file path.
        
        Args:
            file (File): The drawpyo File object to write
            file_path (str): Path where the drawio file should be saved
            
        Returns:
            bool: True if the file was written successfully, False otherwise
            
        Example:
            # Create or modify a drawpyo File
            file = File()
            page = Page("Page 1")
            file.add_page(page)
            
            # Add objects to the page
            obj1 = Object(value="Hello")
            obj1.position = (100, 100)
            obj1.width = 120
            obj1.height = 60
            page.add_object(obj1)
            
            # Write the file to disk
            writer = DrawioWriter()
            success = writer.write_file(file, "output.drawio")
            
            if success:
                print("File written successfully")
            else:
                print("Failed to write file")
        """
        try:
            # Convert the File to XML
            xml_content = self.convert_file_to_xml(file)
            
            # Write the XML to the file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(xml_content)
                
            return True
        except Exception as e:
            print(f"Error writing file: {str(e)}")
            return False
    
    def convert_file_to_xml(self, file):
        """
        Convert a drawpyo File object to drawio XML format.
        
        This method converts a drawpyo File object to a drawio XML string,
        without writing it to disk.
        
        Args:
            file (File): The drawpyo File object to convert
            
        Returns:
            str: The drawio XML content as a string
            
        Example:
            # Create or modify a drawpyo File
            file = File()
            page = Page("Page 1")
            file.add_page(page)
            
            # Add objects to the page
            obj1 = Object(value="Hello")
            obj1.position = (100, 100)
            obj1.width = 120
            obj1.height = 60
            page.add_object(obj1)
            
            # Convert the file to XML
            writer = DrawioWriter()
            xml_content = writer.convert_file_to_xml(file)
            
            # Do something with the XML content
            print(xml_content)
        """
        # Create the root mxfile element
        root = ET.Element("mxfile")
        
        # Set file attributes
        root.set("host", file.host if hasattr(file, "host") else "app.diagrams.net")
        root.set("modified", datetime.now().isoformat())
        root.set("agent", "drawpyo")
        root.set("version", file.version if hasattr(file, "version") else "21.6.5")
        root.set("type", file.type if hasattr(file, "type") else "device")
        
        # Add each page as a diagram
        for page in file.pages:
            diagram_elem = self._convert_page_to_diagram(page)
            root.append(diagram_elem)
        
        # Convert the XML to a pretty string
        xml_str = self._prettify_xml(root)
        
        return xml_str
    
    def _convert_page_to_diagram(self, page):
        """
        Convert a drawpyo Page to a drawio diagram element.
        
        This method converts a drawpyo Page object to an XML Element
        representing a diagram in the drawio format.
        
        Args:
            page (Page): The drawpyo Page object to convert
            
        Returns:
            Element: An XML Element representing the diagram
        """
        # Create the diagram element
        diagram_elem = ET.Element("diagram")
        
        # Set diagram attributes
        diagram_elem.set("id", page.id if hasattr(page, "id") else str(uuid.uuid4()))
        diagram_elem.set("name", page.name)
        
        # Convert the page content to mxGraphModel
        graph_model = self._convert_page_to_graph_model(page)
        
        # Convert the graph model to XML string
        graph_xml = ET.tostring(graph_model, encoding="unicode")
        
        # Compress the content if requested
        if self.compress_content:
            compressed = DrawioDecompressor.compress(graph_xml)
            diagram_elem.text = compressed
        else:
            diagram_elem.text = graph_xml
        
        return diagram_elem
    
    def _convert_page_to_graph_model(self, page):
        """
        Convert a drawpyo Page to an mxGraphModel element.
        
        This method converts a drawpyo Page object to an XML Element
        representing an mxGraphModel in the drawio format.
        
        Args:
            page (Page): The drawpyo Page object to convert
            
        Returns:
            Element: An XML Element representing the mxGraphModel
        """
        # Create the mxGraphModel element
        graph_model = ET.Element("mxGraphModel")
        
        # Set graph model attributes
        graph_model.set("dx", "0")
        graph_model.set("dy", "0")
        graph_model.set("grid", "1")
        graph_model.set("gridSize", "10")
        graph_model.set("guides", "1")
        graph_model.set("tooltips", "1")
        graph_model.set("connect", "1")
        graph_model.set("arrows", "1")
        graph_model.set("fold", "1")
        graph_model.set("page", "1")
        graph_model.set("pageScale", "1")
        graph_model.set("pageWidth", "850")
        graph_model.set("pageHeight", "1100")
        graph_model.set("background", "#ffffff")
        
        # Create the root element
        root = ET.SubElement(graph_model, "root")
        
        # Add the special cells (0 and 1)
        ET.SubElement(root, "mxCell", {"id": "0"})
        ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})
        
        # Add all objects and edges
        self._add_objects_to_root(root, page)
        
        return graph_model
    
    def _add_objects_to_root(self, root, page):
        """
        Add all objects and edges from a page to the root element.
        
        This method converts drawpyo Objects and Edges to mxCell elements
        and adds them to the root element.
        
        Args:
            root (Element): The root XML Element to add objects to
            page (Page): The drawpyo Page containing the objects
        """
        # Create a mapping of objects to IDs
        obj_to_id = {}
        
        # Assign IDs to all objects
        next_id = 2  # IDs 0 and 1 are reserved
        for obj in page.objects:
            obj_to_id[obj] = str(next_id)
            next_id += 1
        
        # Add all objects first
        for obj in page.objects:
            if isinstance(obj, Object) and not isinstance(obj, Edge):
                self._add_object_to_root(root, obj, obj_to_id)
        
        # Then add all edges
        for obj in page.objects:
            if isinstance(obj, Edge):
                self._add_edge_to_root(root, obj, obj_to_id)
    
    def _add_object_to_root(self, root, obj, obj_to_id):
        """
        Add a drawpyo Object to the root element.
        
        This method converts a drawpyo Object to an mxCell element
        and adds it to the root element.
        
        Args:
            root (Element): The root XML Element to add the object to
            obj (Object): The drawpyo Object to convert
            obj_to_id (dict): Mapping of objects to their IDs
        """
        # Get the object ID
        obj_id = obj_to_id[obj]
        
        # Get the parent ID
        parent_id = "1"  # Default parent is 1
        if hasattr(obj, "parent") and obj.parent and obj.parent in obj_to_id:
            parent_id = obj_to_id[obj.parent]
        
        # Create the mxCell element
        cell = ET.SubElement(root, "mxCell", {
            "id": obj_id,
            "parent": parent_id,
            "vertex": "1",
            "value": obj.value if hasattr(obj, "value") and obj.value else ""
        })
        
        # Add style if available
        if hasattr(obj, "get_style_string"):
            style = obj.get_style_string()
            if style:
                cell.set("style", style)
        
        # Add geometry
        if hasattr(obj, "position") and hasattr(obj, "width") and hasattr(obj, "height"):
            x, y = obj.position
            width = obj.width
            height = obj.height
            
            geometry = ET.SubElement(cell, "mxGeometry", {
                "x": str(x),
                "y": str(y),
                "width": str(width),
                "height": str(height),
                "as": "geometry"
            })
    
    def _add_edge_to_root(self, root, edge, obj_to_id):
        """
        Add a drawpyo Edge to the root element.
        
        This method converts a drawpyo Edge to an mxCell element
        and adds it to the root element.
        
        Args:
            root (Element): The root XML Element to add the edge to
            edge (Edge): The drawpyo Edge to convert
            obj_to_id (dict): Mapping of objects to their IDs
        """
        # Get the edge ID
        edge_id = obj_to_id[edge]
        
        # Get the parent ID
        parent_id = "1"  # Default parent is 1
        if hasattr(edge, "parent") and edge.parent and edge.parent in obj_to_id:
            parent_id = obj_to_id[edge.parent]
        
        # Create the mxCell element
        cell_attrs = {
            "id": edge_id,
            "parent": parent_id,
            "edge": "1",
            "value": edge.label if hasattr(edge, "label") and edge.label else ""
        }
        
        # Add source and target if available
        if hasattr(edge, "source") and edge.source and edge.source in obj_to_id:
            cell_attrs["source"] = obj_to_id[edge.source]
        
        if hasattr(edge, "target") and edge.target and edge.target in obj_to_id:
            cell_attrs["target"] = obj_to_id[edge.target]
        
        cell = ET.SubElement(root, "mxCell", cell_attrs)
        
        # Add style if available
        if hasattr(edge, "get_style_string"):
            style = edge.get_style_string()
            if style:
                cell.set("style", style)
        
        # Add geometry (for edge routing)
        geometry = ET.SubElement(cell, "mxGeometry", {
            "relative": "1",
            "as": "geometry"
        })
        
        # Add points if available
        if hasattr(edge, "points") and edge.points:
            points_array = ET.SubElement(geometry, "Array", {"as": "points"})
            
            for point in edge.points:
                x, y = point
                ET.SubElement(points_array, "mxPoint", {
                    "x": str(x),
                    "y": str(y)
                })
    
    def _prettify_xml(self, elem):
        """
        Convert an XML Element to a pretty-printed string.
        
        This method takes an XML Element and returns a nicely formatted
        string representation with proper indentation.
        
        Args:
            elem (Element): The XML Element to prettify
            
        Returns:
            str: The pretty-printed XML string
        """
        # Convert to string
        rough_string = ET.tostring(elem, 'utf-8')
        
        # Parse with minidom
        reparsed = minidom.parseString(rough_string)
        
        # Pretty print with 2-space indentation
        return reparsed.toprettyxml(indent="  ")


class PythonToXmlConverter:
    """
    Class for converting drawpyo objects to drawio XML elements.
    
    This class provides methods to convert drawpyo objects to XML elements
    that can be used to create drawio files. It is used internally by the
    DrawioWriter class but can also be used directly for more control over
    the conversion process.
    
    Example:
        # Create a converter
        converter = PythonToXmlConverter()
        
        # Convert a Page to an mxGraphModel element
        graph_model = converter.convert_page_to_graph_model(page)
        
        # Do something with the XML element
        xml_string = ET.tostring(graph_model, encoding="unicode")
    """
    
    def __init__(self):
        """
        Initialize the converter.
        
        Creates a new PythonToXmlConverter instance for converting drawpyo
        objects to drawio XML elements.
        
        Example:
            converter = PythonToXmlConverter()
        """
        pass
    
    def convert_file_to_mxfile(self, file):
        """
        Convert a drawpyo File to an mxfile XML element.
        
        This method converts a drawpyo File object to an XML Element
        representing an mxfile in the drawio format.
        
        Args:
            file (File): The drawpyo File object to convert
            
        Returns:
            Element: An XML Element representing the mxfile
            
        Example:
            # Convert a File to an mxfile element
            mxfile = converter.convert_file_to_mxfile(file)
            
            # Convert to string
            xml_string = ET.tostring(mxfile, encoding="unicode")
        """
        # Create the root mxfile element
        root = ET.Element("mxfile")
        
        # Set file attributes
        root.set("host", file.host if hasattr(file, "host") else "app.diagrams.net")
        root.set("modified", datetime.now().isoformat())
        root.set("agent", "drawpyo")
        root.set("version", file.version if hasattr(file, "version") else "21.6.5")
        root.set("type", file.type if hasattr(file, "type") else "device")
        
        # Add each page as a diagram
        for page in file.pages:
            diagram_elem = self.convert_page_to_diagram(page)
            root.append(diagram_elem)
        
        return root
    
    def convert_page_to_diagram(self, page, compress=True):
        """
        Convert a drawpyo Page to a diagram XML element.
        
        This method converts a drawpyo Page object to an XML Element
        representing a diagram in the drawio format.
        
        Args:
            page (Page): The drawpyo Page object to convert
            compress (bool): Whether to compress the diagram content
            
        Returns:
            Element: An XML Element representing the diagram
            
        Example:
            # Convert a Page to a diagram element
            diagram = converter.convert_page_to_diagram(page, compress=False)
        """
        # Create the diagram element
        diagram_elem = ET.Element("diagram")
        
        # Set diagram attributes
        diagram_elem.set("id", page.id if hasattr(page, "id") else str(uuid.uuid4()))
        diagram_elem.set("name", page.name)
        
        # Convert the page content to mxGraphModel
        graph_model = self.convert_page_to_graph_model(page)
        
        # Convert the graph model to XML string
        graph_xml = ET.tostring(graph_model, encoding="unicode")
        
        # Compress the content if requested
        if compress:
            compressed = DrawioDecompressor.compress(graph_xml)
            diagram_elem.text = compressed
        else:
            diagram_elem.text = graph_xml
        
        return diagram_elem
    
    def convert_page_to_graph_model(self, page):
        """
        Convert a drawpyo Page to an mxGraphModel XML element.
        
        This method converts a drawpyo Page object to an XML Element
        representing an mxGraphModel in the drawio format.
        
        Args:
            page (Page): The drawpyo Page object to convert
            
        Returns:
            Element: An XML Element representing the mxGraphModel
            
        Example:
            # Convert a Page to an mxGraphModel element
            graph_model = converter.convert_page_to_graph_model(page)
        """
        # Create the mxGraphModel element
        graph_model = ET.Element("mxGraphModel")
        
        # Set graph model attributes
        graph_model.set("dx", "0")
        graph_model.set("dy", "0")
        graph_model.set("grid", "1")
        graph_model.set("gridSize", "10")
        graph_model.set("guides", "1")
        graph_model.set("tooltips", "1")
        graph_model.set("connect", "1")
        graph_model.set("arrows", "1")
        graph_model.set("fold", "1")
        graph_model.set("page", "1")
        graph_model.set("pageScale", "1")
        graph_model.set("pageWidth", "850")
        graph_model.set("pageHeight", "1100")
        graph_model.set("background", "#ffffff")
        
        # Create the root element
        root = ET.SubElement(graph_model, "root")
        
        # Add the special cells (0 and 1)
        ET.SubElement(root, "mxCell", {"id": "0"})
        ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})
        
        # Create a mapping of objects to IDs
        obj_to_id = {}
        
        # Assign IDs to all objects
        next_id = 2  # IDs 0 and 1 are reserved
        for obj in page.objects:
            obj_to_id[obj] = str(next_id)
            next_id += 1
        
        # Add all objects first
        for obj in page.objects:
            if isinstance(obj, Object) and not isinstance(obj, Edge):
                self.convert_object_to_cell(root, obj, obj_to_id)
        
        # Then add all edges
        for obj in page.objects:
            if isinstance(obj, Edge):
                self.convert_edge_to_cell(root, obj, obj_to_id)
        
        return graph_model
    
    def convert_object_to_cell(self, root, obj, obj_to_id):
        """
        Convert a drawpyo Object to an mxCell XML element.
        
        This method converts a drawpyo Object to an XML Element
        representing an mxCell in the drawio format and adds it to
        the root element.
        
        Args:
            root (Element): The root XML Element to add the cell to
            obj (Object): The drawpyo Object to convert
            obj_to_id (dict): Mapping of objects to their IDs
            
        Returns:
            Element: The created mxCell XML Element
            
        Example:
            # Convert an Object to an mxCell element
            cell = converter.convert_object_to_cell(root, obj, obj_to_id)
        """
        # Get the object ID
        obj_id = obj_to_id[obj]
        
        # Get the parent ID
        parent_id = "1"  # Default parent is 1
        if hasattr(obj, "parent") and obj.parent and obj.parent in obj_to_id:
            parent_id = obj_to_id[obj.parent]
        
        # Create the mxCell element
        cell = ET.SubElement(root, "mxCell", {
            "id": obj_id,
            "parent": parent_id,
            "vertex": "1",
            "value": obj.value if hasattr(obj, "value") and obj.value else ""
        })
        
        # Add style if available
        if hasattr(obj, "get_style_string"):
            style = obj.get_style_string()
            if style:
                cell.set("style", style)
        
        # Add geometry
        if hasattr(obj, "position") and hasattr(obj, "width") and hasattr(obj, "height"):
            x, y = obj.position
            width = obj.width
            height = obj.height
            
            geometry = ET.SubElement(cell, "mxGeometry", {
                "x": str(x),
                "y": str(y),
                "width": str(width),
                "height": str(height),
                "as": "geometry"
            })
        
        return cell
    
    def convert_edge_to_cell(self, root, edge, obj_to_id):
        """
        Convert a drawpyo Edge to an mxCell XML element.
        
        This method converts a drawpyo Edge to an XML Element
        representing an mxCell in the drawio format and adds it to
        the root element.
        
        Args:
            root (Element): The root XML Element to add the cell to
            edge (Edge): The drawpyo Edge to convert
            obj_to_id (dict): Mapping of objects to their IDs
            
        Returns:
            Element: The created mxCell XML Element
            
        Example:
            # Convert an Edge to an mxCell element
            cell = converter.convert_edge_to_cell(root, edge, obj_to_id)
        """
        # Get the edge ID
        edge_id = obj_to_id[edge]
        
        # Get the parent ID
        parent_id = "1"  # Default parent is 1
        if hasattr(edge, "parent") and edge.parent and edge.parent in obj_to_id:
            parent_id = obj_to_id[edge.parent]
        
        # Create the mxCell element
        cell_attrs = {
            "id": edge_id,
            "parent": parent_id,
            "edge": "1",
            "value": edge.label if hasattr(edge, "label") and edge.label else ""
        }
        
        # Add source and target if available
        if hasattr(edge, "source") and edge.source and edge.source in obj_to_id:
            cell_attrs["source"] = obj_to_id[edge.source]
        
        if hasattr(edge, "target") and edge.target and edge.target in obj_to_id:
            cell_attrs["target"] = obj_to_id[edge.target]
        
        cell = ET.SubElement(root, "mxCell", cell_attrs)
        
        # Add style if available
        if hasattr(edge, "get_style_string"):
            style = edge.get_style_string()
            if style:
                cell.set("style", style)
        
        # Add geometry (for edge routing)
        geometry = ET.SubElement(cell, "mxGeometry", {
            "relative": "1",
            "as": "geometry"
        })
        
        # Add points if available
        if hasattr(edge, "points") and edge.points:
            points_array = ET.SubElement(geometry, "Array", {"as": "points"})
            
            for point in edge.points:
                x, y = point
                ET.SubElement(points_array, "mxPoint", {
                    "x": str(x),
                    "y": str(y)
                })
        
        return cell
