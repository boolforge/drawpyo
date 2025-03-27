"""
Example script demonstrating the complete workflow of drawpyo extensions.

This script demonstrates how to:
1. Create a new diagram from scratch
2. Read an existing drawio file
3. Modify a diagram
4. Render a diagram to SVG and HTML
5. Save a diagram back to drawio format

It serves as both a test and an example of how to use the extended drawpyo
functionality to work with drawio files programmatically.
"""

import os
import sys
from drawpyo.file import File
from drawpyo.page import Page
from drawpyo.diagram.objects import Object
from drawpyo.diagram.edges import Edge
from drawpyo.reader import DrawioReader
from drawpyo.renderer import DiagramRenderer
from drawpyo.writer import DrawioWriter


def create_example_diagram():
    """Create a simple example diagram from scratch."""
    print("Creating example diagram...")
    
    # Create a new file and page
    file = File()
    page = Page("Example Page")
    file.add_page(page)
    
    # Create some objects
    rect1 = Object(value="Start")
    rect1.position = (100, 100)
    rect1.width = 120
    rect1.height = 60
    rect1.apply_style_string("shape=rectangle;fillColor=#d5e8d4;strokeColor=#82b366;rounded=1;")
    page.add_object(rect1)
    
    rect2 = Object(value="Process")
    rect2.position = (300, 100)
    rect2.width = 120
    rect2.height = 60
    rect2.apply_style_string("shape=rectangle;fillColor=#dae8fc;strokeColor=#6c8ebf;")
    page.add_object(rect2)
    
    rect3 = Object(value="Decision")
    rect3.position = (300, 240)
    rect3.width = 120
    rect3.height = 80
    rect3.apply_style_string("shape=rhombus;fillColor=#fff2cc;strokeColor=#d6b656;")
    page.add_object(rect3)
    
    rect4 = Object(value="End")
    rect4.position = (100, 250)
    rect4.width = 120
    rect4.height = 60
    rect4.apply_style_string("shape=ellipse;fillColor=#f8cecc;strokeColor=#b85450;")
    page.add_object(rect4)
    
    # Create edges between objects
    edge1 = Edge(source=rect1, target=rect2, label="Next")
    edge1.apply_style_string("edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;")
    page.add_object(edge1)
    
    edge2 = Edge(source=rect2, target=rect3, label="Evaluate")
    edge2.apply_style_string("edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;")
    page.add_object(edge2)
    
    edge3 = Edge(source=rect3, target=rect4, label="No")
    edge3.apply_style_string("edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;")
    page.add_object(edge3)
    
    edge4 = Edge(source=rect3, target=rect2, label="Yes")
    edge4.apply_style_string("edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=0;entryX=0.5;entryY=1;")
    page.add_object(edge4)
    
    print("Example diagram created successfully.")
    return file


def save_diagram(file, base_path):
    """Save a diagram to drawio, SVG, and HTML formats."""
    print("Saving diagram...")
    
    # Create output directory if it doesn't exist
    os.makedirs(base_path, exist_ok=True)
    
    # Save as drawio
    drawio_path = os.path.join(base_path, "example.drawio")
    writer = DrawioWriter()
    success = writer.write_file(file, drawio_path)
    if success:
        print(f"Diagram saved to {drawio_path}")
    else:
        print("Failed to save diagram as drawio")
    
    # Render and save as SVG
    svg_path = os.path.join(base_path, "example.svg")
    renderer = DiagramRenderer()
    success = renderer.save_page_as_svg(file.pages[0], svg_path)
    if success:
        print(f"Diagram rendered to SVG: {svg_path}")
    else:
        print("Failed to render diagram as SVG")
    
    # Render and save as HTML
    html_path = os.path.join(base_path, "example.html")
    success = renderer.save_page_as_html(file.pages[0], html_path)
    if success:
        print(f"Diagram rendered to interactive HTML: {html_path}")
    else:
        print("Failed to render diagram as HTML")


def read_and_modify_diagram(file_path):
    """Read an existing drawio file and modify it."""
    print(f"Reading diagram from {file_path}...")
    
    try:
        # Read the file
        file = DrawioReader.read_file(file_path)
        print(f"Successfully read diagram with {len(file.pages)} pages")
        
        # Get the first page
        page = file.pages[0]
        print(f"Page name: {page.name}")
        print(f"Number of objects: {len(page.objects)}")
        
        # Modify the diagram: add a new object
        new_obj = Object(value="New Object")
        new_obj.position = (500, 170)
        new_obj.width = 120
        new_obj.height = 60
        new_obj.apply_style_string("shape=cloud;fillColor=#e1d5e7;strokeColor=#9673a6;")
        page.add_object(new_obj)
        
        # Find objects to connect
        target_obj = None
        for obj in page.objects:
            if isinstance(obj, Object) and not isinstance(obj, Edge):
                if hasattr(obj, 'value') and obj.value == "Process":
                    target_obj = obj
                    break
        
        if target_obj:
            # Add an edge from the new object to an existing one
            new_edge = Edge(source=new_obj, target=target_obj, label="Connect")
            new_edge.apply_style_string("edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;")
            page.add_object(new_edge)
        
        print("Diagram modified successfully.")
        return file
    except Exception as e:
        print(f"Error reading or modifying diagram: {str(e)}")
        return None


def main():
    """Main function to run the example."""
    # Set up paths
    output_dir = "/home/ubuntu/drawpyo-fork/examples/output"
    
    # Create and save an example diagram
    file = create_example_diagram()
    save_diagram(file, output_dir)
    
    # Read back the saved diagram and modify it
    drawio_path = os.path.join(output_dir, "example.drawio")
    modified_file = read_and_modify_diagram(drawio_path)
    
    if modified_file:
        # Save the modified diagram
        save_diagram(modified_file, os.path.join(output_dir, "modified"))
        print("Complete workflow test successful!")
    else:
        print("Workflow test failed at read/modify stage.")


if __name__ == "__main__":
    main()
