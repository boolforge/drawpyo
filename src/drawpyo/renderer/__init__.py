"""
Renderer module for drawio files.

This module provides functionality to render drawio diagrams visually.
It converts drawpyo objects into visual representations that can be
displayed in various formats including SVG, PNG, and interactive HTML.

The renderer handles the visual aspects of drawio elements including:
- Shapes with proper styling (fill color, stroke, etc.)
- Connectors with proper routing and arrow styles
- Text formatting and positioning
- Layout and positioning of all elements

This module bridges the gap between the object model and visual representation,
making it possible to not only manipulate drawio files programmatically but
also visualize the results.
"""

import os
import math
import xml.etree.ElementTree as ET
from ..diagram.objects import Object
from ..diagram.edges import Edge
from .style_parser import StyleParser


class DiagramRenderer:
    """
    Class for rendering drawio diagrams visually.
    
    This class provides methods to render drawpyo objects (File, Page, Object, Edge)
    into visual representations in various formats. It handles the conversion of
    object properties to visual attributes and generates output in formats like
    SVG, PNG, and interactive HTML.
    
    Example:
        # Create a renderer
        renderer = DiagramRenderer()
        
        # Render a page to SVG
        svg_content = renderer.render_page_to_svg(page)
        
        # Save the SVG to a file
        with open("diagram.svg", "w") as f:
            f.write(svg_content)
    """
    
    def __init__(self):
        """
        Initialize the renderer with default settings.
        
        Creates a new DiagramRenderer instance with default rendering settings.
        These settings can be customized after initialization.
        
        Example:
            renderer = DiagramRenderer()
            renderer.scale = 1.5  # Scale the output by 150%
        """
        self.scale = 1.0  # Scale factor for rendering
        self.padding = 20  # Padding around the diagram in pixels
        self.background_color = "#ffffff"  # Default background color
        self.show_grid = False  # Whether to show the grid
        self.grid_size = 10  # Grid size in pixels
        self.grid_color = "#d0d0d0"  # Grid color
    
    def render_page_to_svg(self, page):
        """
        Render a drawpyo Page to SVG format.
        
        This method converts a drawpyo Page object to an SVG string that can
        be displayed in a browser or saved to a file.
        
        Args:
            page (Page): The drawpyo Page object to render
            
        Returns:
            str: The SVG content as a string
            
        Example:
            # Read a drawio file
            file = DrawioReader.read_file("example.drawio")
            
            # Get the first page
            page = file.pages[0]
            
            # Render the page to SVG
            renderer = DiagramRenderer()
            svg_content = renderer.render_page_to_svg(page)
            
            # Save the SVG to a file
            with open("diagram.svg", "w") as f:
                f.write(svg_content)
        """
        # Calculate the bounds of the diagram
        bounds = self._calculate_page_bounds(page)
        width = bounds["width"] + 2 * self.padding
        height = bounds["height"] + 2 * self.padding
        
        # Create the SVG root element
        svg = ET.Element("svg", {
            "xmlns": "http://www.w3.org/2000/svg",
            "width": str(width),
            "height": str(height),
            "viewBox": f"0 0 {width} {height}"
        })
        
        # Add a background rectangle
        ET.SubElement(svg, "rect", {
            "width": "100%",
            "height": "100%",
            "fill": self.background_color
        })
        
        # Add a group for the diagram content with a transform to apply padding
        g = ET.SubElement(svg, "g", {
            "transform": f"translate({self.padding},{self.padding})"
        })
        
        # Draw grid if enabled
        if self.show_grid:
            self._draw_grid(g, bounds)
        
        # Draw all objects
        for obj in page.objects:
            if isinstance(obj, Object):
                self._render_object_to_svg(obj, g)
        
        # Draw all edges (after objects so they appear on top)
        for obj in page.objects:
            if isinstance(obj, Edge):
                self._render_edge_to_svg(obj, g)
        
        # Convert the XML to a string
        return ET.tostring(svg, encoding="unicode")
    
    def render_page_to_html(self, page, include_interactivity=True):
        """
        Render a drawpyo Page to an HTML document.
        
        This method converts a drawpyo Page object to an HTML string that can
        be displayed in a browser. The HTML can optionally include JavaScript
        for interactive features like zooming and panning.
        
        Args:
            page (Page): The drawpyo Page object to render
            include_interactivity (bool): Whether to include interactive features
            
        Returns:
            str: The HTML content as a string
            
        Example:
            # Read a drawio file
            file = DrawioReader.read_file("example.drawio")
            
            # Get the first page
            page = file.pages[0]
            
            # Render the page to interactive HTML
            renderer = DiagramRenderer()
            html_content = renderer.render_page_to_html(page)
            
            # Save the HTML to a file
            with open("diagram.html", "w") as f:
                f.write(html_content)
        """
        # Get the SVG content
        svg_content = self.render_page_to_svg(page)
        
        # Create the HTML document
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{page.name}</title>
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; }}
        #diagram-container {{ width: 100%; height: 100vh; }}
    </style>
</head>
<body>
    <div id="diagram-container">
        {svg_content}
    </div>
"""
        
        # Add interactive features if requested
        if include_interactivity:
            html += """
    <script>
        // Add zooming and panning functionality
        (function() {
            const svg = document.querySelector('svg');
            let isPanning = false;
            let startPoint = { x: 0, y: 0 };
            let currentTranslate = { x: 0, y: 0 };
            let scale = 1;
            
            // Add event listeners for zooming
            svg.addEventListener('wheel', function(event) {
                event.preventDefault();
                const delta = event.deltaY;
                const scaleAmount = delta > 0 ? 0.9 : 1.1;
                scale *= scaleAmount;
                
                // Apply the scale transform
                const g = svg.querySelector('g');
                g.setAttribute('transform', 
                    `translate(${currentTranslate.x},${currentTranslate.y}) scale(${scale})`);
            });
            
            // Add event listeners for panning
            svg.addEventListener('mousedown', function(event) {
                if (event.button === 0) {  // Left mouse button
                    isPanning = true;
                    startPoint = { x: event.clientX, y: event.clientY };
                }
            });
            
            svg.addEventListener('mousemove', function(event) {
                if (isPanning) {
                    const dx = event.clientX - startPoint.x;
                    const dy = event.clientY - startPoint.y;
                    
                    currentTranslate.x += dx;
                    currentTranslate.y += dy;
                    
                    startPoint = { x: event.clientX, y: event.clientY };
                    
                    // Apply the transform
                    const g = svg.querySelector('g');
                    g.setAttribute('transform', 
                        `translate(${currentTranslate.x},${currentTranslate.y}) scale(${scale})`);
                }
            });
            
            svg.addEventListener('mouseup', function() {
                isPanning = false;
            });
            
            svg.addEventListener('mouseleave', function() {
                isPanning = false;
            });
        })();
    </script>
"""
        
        html += """
</body>
</html>
"""
        
        return html
    
    def save_page_as_svg(self, page, file_path):
        """
        Render a drawpyo Page and save it as an SVG file.
        
        This method renders a drawpyo Page object to SVG and saves it to a file.
        
        Args:
            page (Page): The drawpyo Page object to render
            file_path (str): Path where the SVG file should be saved
            
        Returns:
            bool: True if the file was saved successfully, False otherwise
            
        Example:
            # Read a drawio file
            file = DrawioReader.read_file("example.drawio")
            
            # Get the first page
            page = file.pages[0]
            
            # Render and save the page as SVG
            renderer = DiagramRenderer()
            success = renderer.save_page_as_svg(page, "diagram.svg")
            
            if success:
                print(f"SVG saved to diagram.svg")
            else:
                print(f"Failed to save SVG")
        """
        try:
            svg_content = self.render_page_to_svg(page)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(svg_content)
                
            return True
        except Exception as e:
            print(f"Error saving SVG: {str(e)}")
            return False
    
    def save_page_as_html(self, page, file_path, include_interactivity=True):
        """
        Render a drawpyo Page and save it as an HTML file.
        
        This method renders a drawpyo Page object to HTML and saves it to a file.
        The HTML can optionally include JavaScript for interactive features.
        
        Args:
            page (Page): The drawpyo Page object to render
            file_path (str): Path where the HTML file should be saved
            include_interactivity (bool): Whether to include interactive features
            
        Returns:
            bool: True if the file was saved successfully, False otherwise
            
        Example:
            # Read a drawio file
            file = DrawioReader.read_file("example.drawio")
            
            # Get the first page
            page = file.pages[0]
            
            # Render and save the page as interactive HTML
            renderer = DiagramRenderer()
            success = renderer.save_page_as_html(page, "diagram.html")
            
            if success:
                print(f"HTML saved to diagram.html")
            else:
                print(f"Failed to save HTML")
        """
        try:
            html_content = self.render_page_to_html(page, include_interactivity)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
                
            return True
        except Exception as e:
            print(f"Error saving HTML: {str(e)}")
            return False
    
    def _calculate_page_bounds(self, page):
        """
        Calculate the bounds of a page.
        
        This method calculates the minimum and maximum coordinates of all objects
        in a page, which is used to determine the size of the output SVG.
        
        Args:
            page (Page): The drawpyo Page object
            
        Returns:
            dict: A dictionary with the bounds information:
                {
                    "min_x": float,
                    "min_y": float,
                    "max_x": float,
                    "max_y": float,
                    "width": float,
                    "height": float
                }
        """
        min_x = float('inf')
        min_y = float('inf')
        max_x = float('-inf')
        max_y = float('-inf')
        
        # Check all objects
        for obj in page.objects:
            if isinstance(obj, Object):
                x, y = obj.position
                width = obj.width
                height = obj.height
                
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x + width)
                max_y = max(max_y, y + height)
        
        # If there are no objects, use default bounds
        if min_x == float('inf'):
            min_x = 0
            min_y = 0
            max_x = 100
            max_y = 100
        
        return {
            "min_x": min_x,
            "min_y": min_y,
            "max_x": max_x,
            "max_y": max_y,
            "width": max_x - min_x,
            "height": max_y - min_y
        }
    
    def _draw_grid(self, parent_element, bounds):
        """
        Draw a grid in the background of the diagram.
        
        This method adds grid lines to the SVG to help with visual alignment.
        
        Args:
            parent_element (Element): The SVG element to add the grid to
            bounds (dict): The bounds of the diagram
        """
        grid_group = ET.SubElement(parent_element, "g", {
            "class": "grid",
            "stroke": self.grid_color,
            "stroke-width": "0.5"
        })
        
        # Calculate grid lines
        min_x = bounds["min_x"]
        min_y = bounds["min_y"]
        max_x = bounds["max_x"]
        max_y = bounds["max_y"]
        
        # Round to nearest grid size
        min_x = math.floor(min_x / self.grid_size) * self.grid_size
        min_y = math.floor(min_y / self.grid_size) * self.grid_size
        max_x = math.ceil(max_x / self.grid_size) * self.grid_size
        max_y = math.ceil(max_y / self.grid_size) * self.grid_size
        
        # Draw vertical grid lines
        for x in range(min_x, max_x + 1, self.grid_size):
            ET.SubElement(grid_group, "line", {
                "x1": str(x),
                "y1": str(min_y),
                "x2": str(x),
                "y2": str(max_y)
            })
        
        # Draw horizontal grid lines
        for y in range(min_y, max_y + 1, self.grid_size):
            ET.SubElement(grid_group, "line", {
                "x1": str(min_x),
                "y1": str(y),
                "x2": str(max_x),
                "y2": str(y)
            })
    
    def _render_object_to_svg(self, obj, parent_element):
        """
        Render a drawpyo Object to SVG.
        
        This method converts a drawpyo Object to SVG elements and adds them
        to the parent SVG element.
        
        Args:
            obj (Object): The drawpyo Object to render
            parent_element (Element): The SVG element to add the object to
        """
        x, y = obj.position
        width = obj.width
        height = obj.height
        
        # Get style properties
        style = obj.get_style_string()
        style_dict = StyleParser.parse_style(style)
        
        # Get shape type
        shape_type = style_dict.get("shape", "rectangle")
        
        # Create a group for this object
        g = ET.SubElement(parent_element, "g", {
            "class": "object",
            "data-id": str(id(obj))
        })
        
        # Create the shape element based on the shape type
        if shape_type == "ellipse":
            shape = ET.SubElement(g, "ellipse", {
                "cx": str(x + width / 2),
                "cy": str(y + height / 2),
                "rx": str(width / 2),
                "ry": str(height / 2)
            })
        elif shape_type == "rhombus":
            points = f"{x},{y + height/2} {x + width/2},{y} {x + width},{y + height/2} {x + width/2},{y + height}"
            shape = ET.SubElement(g, "polygon", {
                "points": points
            })
        elif shape_type == "triangle":
            points = f"{x + width/2},{y} {x + width},{y + height} {x},{y + height}"
            shape = ET.SubElement(g, "polygon", {
                "points": points
            })
        elif shape_type == "hexagon":
            w4 = width / 4
            points = f"{x + w4},{y} {x + width - w4},{y} {x + width},{y + height/2} {x + width - w4},{y + height} {x + w4},{y + height} {x},{y + height/2}"
            shape = ET.SubElement(g, "polygon", {
                "points": points
            })
        elif shape_type == "cylinder":
            # Cylinders are complex, use a group with multiple elements
            cylinder_g = ET.SubElement(g, "g")
            
            # Draw the main rectangle
            ET.SubElement(cylinder_g, "rect", {
                "x": str(x),
                "y": str(y + height * 0.1),
                "width": str(width),
                "height": str(height * 0.8)
            })
            
            # Draw the top ellipse
            ET.SubElement(cylinder_g, "ellipse", {
                "cx": str(x + width / 2),
                "cy": str(y + height * 0.1),
                "rx": str(width / 2),
                "ry": str(height * 0.1)
            })
            
            # Draw the bottom ellipse
            ET.SubElement(cylinder_g, "ellipse", {
                "cx": str(x + width / 2),
                "cy": str(y + height * 0.9),
                "rx": str(width / 2),
                "ry": str(height * 0.1)
            })
            
            shape = cylinder_g
        else:  # Default to rectangle
            # Check if rounded
            rounded = style_dict.get("rounded", "0")
            rx = "5" if rounded == "1" else "0"
            
            shape = ET.SubElement(g, "rect", {
                "x": str(x),
                "y": str(y),
                "width": str(width),
                "height": str(height),
                "rx": rx
            })
        
        # Apply style attributes
        fill_color = style_dict.get("fillColor", "#ffffff")
        stroke_color = style_dict.get("strokeColor", "#000000")
        stroke_width = style_dict.get("strokeWidth", "1")
        
        # If shape is a group, apply styles to all children
        if isinstance(shape, ET.Element) and shape.tag == "g":
            for child in shape:
                child.set("fill", fill_color)
                child.set("stroke", stroke_color)
                child.set("stroke-width", str(stroke_width))
        else:
            shape.set("fill", fill_color)
            shape.set("stroke", stroke_color)
            shape.set("stroke-width", str(stroke_width))
        
        # Add text if present
        if obj.value:
            text = ET.SubElement(g, "text", {
                "x": str(x + width / 2),
                "y": str(y + height / 2),
                "text-anchor": "middle",
                "dominant-baseline": "middle",
                "font-family": style_dict.get("fontFamily", "Arial"),
                "font-size": str(style_dict.get("fontSize", "12")),
                "fill": style_dict.get("fontColor", "#000000")
            })
            text.text = obj.value
    
    def _render_edge_to_svg(self, edge, parent_element):
        """
        Render a drawpyo Edge to SVG.
        
        This method converts a drawpyo Edge to SVG elements and adds them
        to the parent SVG element.
        
        Args:
            edge (Edge): The drawpyo Edge to render
            parent_element (Element): The SVG element to add the edge to
        """
        # Skip edges without source or target
        if not edge.source or not edge.target:
            return
        
        # Get source and target positions
        source_x, source_y = edge.source.position
        source_width = edge.source.width
        source_height = edge.source.height
        
        target_x, target_y = edge.target.position
        target_width = edge.target.width
        target_height = edge.target.height
        
        # Calculate center points
        source_center_x = source_x + source_width / 2
        source_center_y = source_y + source_height / 2
        
        target_center_x = target_x + target_width / 2
        target_center_y = target_y + target_height / 2
        
        # Get style properties
        style = edge.get_style_string()
        style_dict = StyleParser.parse_style(style)
        
        # Get edge style
        edge_style = style_dict.get("edgeStyle", "orthogonalEdgeStyle")
        
        # Create a group for this edge
        g = ET.SubElement(parent_element, "g", {
            "class": "edge",
            "data-id": str(id(edge))
        })
        
        # Calculate path based on edge style
        if edge_style == "orthogonalEdgeStyle":
            # Orthogonal edges have right angles
            path_data = self._calculate_orthogonal_path(
                source_x, source_y, source_width, source_height,
                target_x, target_y, target_width, target_height
            )
        elif edge_style == "elbowEdgeStyle":
            # Elbow edges have a single bend
            path_data = self._calculate_elbow_path(
                source_x, source_y, source_width, source_height,
                target_x, target_y, target_width, target_height
            )
        elif edge_style == "entityRelationEdgeStyle":
            # Entity relation edges are similar to elbow but with specific rules
            path_data = self._calculate_entity_relation_path(
                source_x, source_y, source_width, source_height,
                target_x, target_y, target_width, target_height
            )
        else:  # Default to straight line
            # Calculate intersection points with the shape boundaries
            start_point = self._calculate_intersection_point(
                source_center_x, source_center_y,
                target_center_x, target_center_y,
                source_x, source_y, source_width, source_height
            )
            
            end_point = self._calculate_intersection_point(
                target_center_x, target_center_y,
                source_center_x, source_center_y,
                target_x, target_y, target_width, target_height
            )
            
            path_data = f"M {start_point[0]},{start_point[1]} L {end_point[0]},{end_point[1]}"
        
        # Create the path element
        path = ET.SubElement(g, "path", {
            "d": path_data,
            "fill": "none",
            "stroke": style_dict.get("strokeColor", "#000000"),
            "stroke-width": str(style_dict.get("strokeWidth", "1"))
        })
        
        # Add dashed style if specified
        if style_dict.get("dashed", "0") == "1":
            path.set("stroke-dasharray", "5,5")
        
        # Add arrows if specified
        start_arrow = style_dict.get("startArrow", "none")
        end_arrow = style_dict.get("endArrow", "classic")
        
        if start_arrow != "none":
            self._add_arrow_marker(g, "start-arrow", start_arrow, style_dict)
            path.set("marker-start", "url(#start-arrow)")
        
        if end_arrow != "none":
            self._add_arrow_marker(g, "end-arrow", end_arrow, style_dict)
            path.set("marker-end", "url(#end-arrow)")
        
        # Add label if present
        if edge.label:
            # Calculate label position (midpoint of the edge)
            label_x = (source_center_x + target_center_x) / 2
            label_y = (source_center_y + target_center_y) / 2
            
            # Add a white background for better readability
            ET.SubElement(g, "rect", {
                "x": str(label_x - 20),
                "y": str(label_y - 10),
                "width": "40",
                "height": "20",
                "fill": "white",
                "stroke": "none"
            })
            
            text = ET.SubElement(g, "text", {
                "x": str(label_x),
                "y": str(label_y),
                "text-anchor": "middle",
                "dominant-baseline": "middle",
                "font-family": style_dict.get("fontFamily", "Arial"),
                "font-size": str(style_dict.get("fontSize", "12")),
                "fill": style_dict.get("fontColor", "#000000")
            })
            text.text = edge.label
    
    def _calculate_orthogonal_path(self, source_x, source_y, source_width, source_height,
                                  target_x, target_y, target_width, target_height):
        """
        Calculate an orthogonal path between two rectangles.
        
        This method calculates a path with right angles between the source and target.
        
        Args:
            source_x, source_y: Top-left coordinates of the source rectangle
            source_width, source_height: Dimensions of the source rectangle
            target_x, target_y: Top-left coordinates of the target rectangle
            target_width, target_height: Dimensions of the target rectangle
            
        Returns:
            str: SVG path data string
        """
        # Calculate center points
        source_center_x = source_x + source_width / 2
        source_center_y = source_y + source_height / 2
        
        target_center_x = target_x + target_width / 2
        target_center_y = target_y + target_height / 2
        
        # Determine which sides to connect based on relative positions
        if abs(source_center_x - target_center_x) > abs(source_center_y - target_center_y):
            # Connect horizontally (left/right sides)
            if source_center_x < target_center_x:
                # Source is to the left of target
                start_x = source_x + source_width
                start_y = source_center_y
                end_x = target_x
                end_y = target_center_y
            else:
                # Source is to the right of target
                start_x = source_x
                start_y = source_center_y
                end_x = target_x + target_width
                end_y = target_center_y
        else:
            # Connect vertically (top/bottom sides)
            if source_center_y < target_center_y:
                # Source is above target
                start_x = source_center_x
                start_y = source_y + source_height
                end_x = target_center_x
                end_y = target_y
            else:
                # Source is below target
                start_x = source_center_x
                start_y = source_y
                end_x = target_center_x
                end_y = target_y + target_height
        
        # Calculate the midpoint for the orthogonal path
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        
        # Create the path data
        return f"M {start_x},{start_y} L {mid_x},{start_y} L {mid_x},{end_y} L {end_x},{end_y}"
    
    def _calculate_elbow_path(self, source_x, source_y, source_width, source_height,
                             target_x, target_y, target_width, target_height):
        """
        Calculate an elbow path between two rectangles.
        
        This method calculates a path with a single bend between the source and target.
        
        Args:
            source_x, source_y: Top-left coordinates of the source rectangle
            source_width, source_height: Dimensions of the source rectangle
            target_x, target_y: Top-left coordinates of the target rectangle
            target_width, target_height: Dimensions of the target rectangle
            
        Returns:
            str: SVG path data string
        """
        # Calculate center points
        source_center_x = source_x + source_width / 2
        source_center_y = source_y + source_height / 2
        
        target_center_x = target_x + target_width / 2
        target_center_y = target_y + target_height / 2
        
        # Determine which sides to connect based on relative positions
        if abs(source_center_x - target_center_x) > abs(source_center_y - target_center_y):
            # Connect horizontally (left/right sides)
            if source_center_x < target_center_x:
                # Source is to the left of target
                start_x = source_x + source_width
                start_y = source_center_y
                end_x = target_x
                end_y = target_center_y
            else:
                # Source is to the right of target
                start_x = source_x
                start_y = source_center_y
                end_x = target_x + target_width
                end_y = target_center_y
                
            # Create the path data with a horizontal bend
            return f"M {start_x},{start_y} L {(start_x + end_x) / 2},{start_y} L {(start_x + end_x) / 2},{end_y} L {end_x},{end_y}"
        else:
            # Connect vertically (top/bottom sides)
            if source_center_y < target_center_y:
                # Source is above target
                start_x = source_center_x
                start_y = source_y + source_height
                end_x = target_center_x
                end_y = target_y
            else:
                # Source is below target
                start_x = source_center_x
                start_y = source_y
                end_x = target_center_x
                end_y = target_y + target_height
                
            # Create the path data with a vertical bend
            return f"M {start_x},{start_y} L {start_x},{(start_y + end_y) / 2} L {end_x},{(start_y + end_y) / 2} L {end_x},{end_y}"
    
    def _calculate_entity_relation_path(self, source_x, source_y, source_width, source_height,
                                       target_x, target_y, target_width, target_height):
        """
        Calculate an entity relation path between two rectangles.
        
        This method calculates a path with specific rules for entity relationship diagrams.
        
        Args:
            source_x, source_y: Top-left coordinates of the source rectangle
            source_width, source_height: Dimensions of the source rectangle
            target_x, target_y: Top-left coordinates of the target rectangle
            target_width, target_height: Dimensions of the target rectangle
            
        Returns:
            str: SVG path data string
        """
        # For simplicity, use the elbow path for now
        # In a real implementation, this would have specific rules for ER diagrams
        return self._calculate_elbow_path(
            source_x, source_y, source_width, source_height,
            target_x, target_y, target_width, target_height
        )
    
    def _calculate_intersection_point(self, line_start_x, line_start_y, line_end_x, line_end_y,
                                     rect_x, rect_y, rect_width, rect_height):
        """
        Calculate the intersection point of a line with a rectangle.
        
        This method finds where a line from the center of one shape to the center
        of another intersects with the boundary of the first shape.
        
        Args:
            line_start_x, line_start_y: Start point of the line
            line_end_x, line_end_y: End point of the line
            rect_x, rect_y: Top-left coordinates of the rectangle
            rect_width, rect_height: Dimensions of the rectangle
            
        Returns:
            tuple: (x, y) coordinates of the intersection point
        """
        # Calculate the rectangle's corners
        left = rect_x
        right = rect_x + rect_width
        top = rect_y
        bottom = rect_y + rect_height
        
        # Calculate the direction vector of the line
        dx = line_end_x - line_start_x
        dy = line_end_y - line_start_y
        
        # Normalize the direction vector
        length = math.sqrt(dx * dx + dy * dy)
        if length > 0:
            dx /= length
            dy /= length
        
        # Calculate intersection with each edge of the rectangle
        # and find the closest valid intersection
        
        # Intersection with left edge
        if dx != 0:
            t_left = (left - line_start_x) / dx
            y_left = line_start_y + t_left * dy
            if top <= y_left <= bottom and t_left >= 0:
                return (left, y_left)
        
        # Intersection with right edge
        if dx != 0:
            t_right = (right - line_start_x) / dx
            y_right = line_start_y + t_right * dy
            if top <= y_right <= bottom and t_right >= 0:
                return (right, y_right)
        
        # Intersection with top edge
        if dy != 0:
            t_top = (top - line_start_y) / dy
            x_top = line_start_x + t_top * dx
            if left <= x_top <= right and t_top >= 0:
                return (x_top, top)
        
        # Intersection with bottom edge
        if dy != 0:
            t_bottom = (bottom - line_start_y) / dy
            x_bottom = line_start_x + t_bottom * dx
            if left <= x_bottom <= right and t_bottom >= 0:
                return (x_bottom, bottom)
        
        # If no intersection is found, return the center of the rectangle
        # (this should not happen if the line starts from the center)
        return (rect_x + rect_width / 2, rect_y + rect_height / 2)
    
    def _add_arrow_marker(self, parent_element, marker_id, arrow_type, style_dict):
        """
        Add an arrow marker definition to the SVG.
        
        This method creates an SVG marker element for arrow heads and adds it
        to the parent element.
        
        Args:
            parent_element (Element): The SVG element to add the marker to
            marker_id (str): The ID to use for the marker
            arrow_type (str): The type of arrow (classic, block, open, etc.)
            style_dict (dict): Style properties for the arrow
        """
        # Create a defs element if it doesn't exist
        defs = parent_element.find("defs")
        if defs is None:
            defs = ET.SubElement(parent_element, "defs")
        
        # Create the marker element
        marker = ET.SubElement(defs, "marker", {
            "id": marker_id,
            "viewBox": "0 0 10 10",
            "refX": "10",
            "refY": "5",
            "markerWidth": "6",
            "markerHeight": "6",
            "orient": "auto"
        })
        
        # Get arrow color
        stroke_color = style_dict.get("strokeColor", "#000000")
        fill_color = stroke_color
        if arrow_type == "open":
            fill_color = "none"
        
        # Create the arrow path based on the type
        if arrow_type == "classic":
            # Classic arrow (triangle)
            path = ET.SubElement(marker, "path", {
                "d": "M 0 0 L 10 5 L 0 10 z",
                "fill": fill_color,
                "stroke": stroke_color
            })
        elif arrow_type == "block":
            # Block arrow (rectangle)
            path = ET.SubElement(marker, "path", {
                "d": "M 0 0 L 10 0 L 10 10 L 0 10 z",
                "fill": fill_color,
                "stroke": stroke_color
            })
        elif arrow_type == "open":
            # Open arrow (V shape)
            path = ET.SubElement(marker, "path", {
                "d": "M 0 0 L 10 5 L 0 10",
                "fill": "none",
                "stroke": stroke_color
            })
        elif arrow_type == "oval":
            # Oval arrow (circle)
            circle = ET.SubElement(marker, "circle", {
                "cx": "5",
                "cy": "5",
                "r": "5",
                "fill": fill_color,
                "stroke": stroke_color
            })
        elif arrow_type == "diamond":
            # Diamond arrow
            path = ET.SubElement(marker, "path", {
                "d": "M 0 5 L 5 0 L 10 5 L 5 10 z",
                "fill": fill_color,
                "stroke": stroke_color
            })
        else:
            # Default to classic arrow
            path = ET.SubElement(marker, "path", {
                "d": "M 0 0 L 10 5 L 0 10 z",
                "fill": fill_color,
                "stroke": stroke_color
            })
