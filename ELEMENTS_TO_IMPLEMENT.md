# Elements to Implement in drawpyo

Based on the analysis of drawpyo's current capabilities and the drawio format, the following elements need to be implemented to extend drawpyo's functionality.

## 1. Shape Libraries

### UML Shapes
- Class diagrams
- Use case diagrams
- Sequence diagrams
- Activity diagrams
- State diagrams
- Component diagrams
- Deployment diagrams

### Network Shapes
- Network devices (routers, switches, firewalls)
- Cloud components
- Server components
- Client devices

### Cloud Provider Shapes
- AWS icons
- Azure icons
- GCP icons

### BPMN Shapes
- Events (start, intermediate, end)
- Activities (task, subprocess)
- Gateways (exclusive, parallel, inclusive)
- Connecting objects
- Swimlanes and pools

### ER Diagram Shapes
- Entity shapes
- Relationship shapes
- Attribute shapes
- Cardinality indicators

### Circuit Shapes
- Logic gates
- Resistors, capacitors, inductors
- Switches, diodes, transistors
- Power sources

## 2. Complex Elements

### Tables
- Table structure
- Cell formatting
- Row and column spans

### Images
- Image import and embedding
- Image positioning and sizing
- Image formatting

### Complex Containers
- Swimlanes
- Kanban boards
- Mindmap nodes
- Treemap containers

### Custom Shapes
- Shape definition from SVG
- Custom shape libraries
- Shape editing capabilities

## 3. Advanced Connectors

### Connector Types
- Curved connectors
- Bezier curve connectors
- Arc connectors
- Entity-relationship connectors

### Connector Features
- Multiple labels on connectors
- Custom connection points
- Waypoints and routing
- Jump styles for crossing connectors

## 4. Advanced Styling

### Fill Styles
- Gradient fills (linear, radial)
- Pattern fills
- Image fills
- Opacity and transparency

### Line Styles
- Custom dash patterns
- Line caps and joins
- Line decorations
- Arrow customization

### Text Formatting
- Rich text formatting
- Font families and sizes
- Text alignment and orientation
- Text overflow handling

## 5. File Operations

### Reading Existing Files
- Parse XML structure
- Handle compressed content (base64 + deflate)
- Extract diagram elements
- Convert to drawpyo objects

### Advanced File Features
- Multiple pages support
- Layers support
- Background grid customization
- Page size and orientation

## Implementation Priority

1. **High Priority**
   - Reading existing drawio files
   - UML shape libraries
   - Advanced connectors
   - Basic styling improvements

2. **Medium Priority**
   - Network and cloud shapes
   - Complex containers
   - Text formatting enhancements
   - Multiple labels on connectors

3. **Lower Priority**
   - Circuit shapes
   - Custom shape libraries
   - Advanced styling (gradients, patterns)
   - Tables and embedded images
