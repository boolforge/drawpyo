# Design for drawpyo Extensions

This document outlines the design for extending drawpyo to support more elements of the drawio format.

## Architecture Overview

The extensions will follow the existing architecture of drawpyo, preserving all current functionality while adding new capabilities. The design focuses on:

1. Maintaining backward compatibility
2. Following the existing class hierarchy
3. Using consistent naming conventions
4. Implementing features in a modular way

## New Components

### 1. File Reader Module

A new module for reading existing drawio files will be added:

```
src/drawpyo/reader/
├── __init__.py
├── parser.py         # Main parser for drawio XML
├── decompressor.py   # Handles base64+deflate content
├── converter.py      # Converts XML to drawpyo objects
└── validator.py      # Validates drawio file structure
```

#### Key Classes:

- `DrawioReader`: Main class for reading drawio files
- `DrawioDecompressor`: Handles compressed content
- `XmlToPythonConverter`: Converts XML elements to drawpyo objects

### 2. Shape Libraries

New shape libraries will be added as TOML files:

```
src/drawpyo/shape_libraries/
├── uml.toml          # UML diagram shapes
├── network.toml      # Network diagram shapes
├── aws.toml          # AWS icons
├── azure.toml        # Azure icons
├── gcp.toml          # GCP icons
├── bpmn.toml         # BPMN shapes
├── er.toml           # ER diagram shapes
└── circuit.toml      # Circuit diagram shapes
```

### 3. Extended Object Classes

New classes will be added to support complex elements:

```python
# Table support
class Table(Object):
    """Represents a table in a drawio diagram"""
    
class TableCell(Object):
    """Represents a cell in a table"""

# Image support
class Image(Object):
    """Represents an embedded image"""
    
# Container support
class Container(Object):
    """Base class for container objects"""
    
class Swimlane(Container):
    """Represents a swimlane container"""
    
class KanbanBoard(Container):
    """Represents a Kanban board"""
```

### 4. Extended Edge Classes

New classes for advanced connectors:

```python
class CurvedEdge(Edge):
    """Represents a curved connector"""
    
class BezierEdge(Edge):
    """Represents a Bezier curve connector"""
    
class ArcEdge(Edge):
    """Represents an arc connector"""
    
class ERConnector(Edge):
    """Represents an entity-relationship connector"""
```

### 5. Style Enhancements

Extensions to existing style handling:

```python
class GradientFill:
    """Handles gradient fill styles"""
    
class PatternFill:
    """Handles pattern fill styles"""
    
class RichTextFormat(TextFormat):
    """Extended text formatting with rich text support"""
```

## Implementation Approach

### Phase 1: File Reading Capability

1. Implement the `DrawioReader` class to parse drawio XML
2. Add decompression support for base64+deflate content
3. Create converters to transform XML to drawpyo objects
4. Add validation to ensure proper file structure

### Phase 2: UML and Basic Shape Libraries

1. Create UML shape library (uml.toml)
2. Implement necessary object classes for UML elements
3. Add support for UML-specific connectors
4. Create basic network shape library

### Phase 3: Advanced Connectors

1. Implement curved and Bezier connectors
2. Add support for multiple labels on connectors
3. Enhance connector routing capabilities
4. Implement jump styles for crossing connectors

### Phase 4: Complex Elements

1. Add support for tables and cells
2. Implement image embedding
3. Create container classes (swimlanes, etc.)
4. Add support for custom shapes

### Phase 5: Advanced Styling

1. Implement gradient and pattern fills
2. Enhance text formatting capabilities
3. Add support for line style customization
4. Implement opacity and transparency

## API Extensions

### Reading Files

```python
# Current API for creating files
file = File("example.drawio")
page = Page("Page 1")
file.add_page(page)

# New API for reading files
file = DrawioReader.read_file("existing.drawio")
pages = file.pages  # Access existing pages
```

### Creating UML Elements

```python
# Creating UML class
class_obj = UMLClass("MyClass", attributes=["attr1: int", "attr2: string"], 
                     methods=["method1()", "method2(param)"])
page.add_object(class_obj)

# Creating relationships
relationship = UMLRelationship(source=class1, target=class2, 
                              type="inheritance")
page.add_object(relationship)
```

### Working with Tables

```python
# Creating a table
table = Table(rows=3, columns=4)
table.set_cell_value(0, 0, "Header 1")
table.set_cell_value(0, 1, "Header 2")
page.add_object(table)
```

### Advanced Styling

```python
# Adding gradient fill
shape = Object("My Shape")
shape.fill = GradientFill(start_color="#ff0000", end_color="#0000ff", 
                         direction="vertical")

# Rich text formatting
text = RichTextFormat()
text.add_bold("Bold text")
text.add_italic("Italic text")
shape.text_format = text
```

## Compatibility Considerations

1. All new features will be optional, not breaking existing code
2. Default values will maintain backward compatibility
3. New parameters will have sensible defaults
4. Documentation will clearly indicate new vs. existing functionality

## Testing Strategy

1. Unit tests for each new component
2. Integration tests for interactions between components
3. Round-trip tests (create → save → read → compare)
4. Compatibility tests with existing drawio files
