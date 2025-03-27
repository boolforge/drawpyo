# Drawpyo Extensions - Documentación Completa

## Introducción

Esta documentación describe las extensiones implementadas para la biblioteca drawpyo, que permiten trabajar con archivos drawio de manera completa. Las extensiones añaden capacidades para:

1. **Leer** archivos drawio existentes
2. **Representar** visualmente diagramas en formatos SVG y HTML
3. **Modificar** diagramas programáticamente
4. **Escribir** diagramas modificados de vuelta a archivos drawio

Estas extensiones convierten a drawpyo en una solución completa para trabajar con diagramas drawio desde Python, sin necesidad de utilizar la interfaz gráfica de draw.io.

## Estructura de Módulos

Las extensiones se organizan en tres módulos principales:

1. **reader**: Para leer y parsear archivos drawio
2. **renderer**: Para renderizar diagramas en formatos visuales
3. **writer**: Para escribir diagramas a archivos drawio

### Módulo Reader

El módulo reader proporciona funcionalidad para leer archivos drawio existentes y convertirlos a objetos drawpyo. Está compuesto por:

- **DrawioReader**: Clase principal para leer archivos drawio
- **DrawioParser**: Parsea archivos drawio y extrae su contenido
- **DrawioDecompressor**: Maneja la compresión/descompresión de contenido
- **XmlToPythonConverter**: Convierte elementos XML a objetos drawpyo
- **StyleParser**: Parsea y manipula cadenas de estilo de drawio

#### Uso Básico del Reader

```python
from drawpyo.reader import DrawioReader

# Leer un archivo drawio
file = DrawioReader.read_file("ejemplo.drawio")

# Acceder a las páginas y objetos
for page in file.pages:
    print(f"Página: {page.name}")
    for obj in page.objects:
        print(f"  Objeto: {obj}")
```

### Módulo Renderer

El módulo renderer proporciona funcionalidad para renderizar diagramas drawio en formatos visuales como SVG y HTML. Está compuesto por:

- **DiagramRenderer**: Clase principal para renderizar diagramas

#### Uso Básico del Renderer

```python
from drawpyo.reader import DrawioReader
from drawpyo.renderer import DiagramRenderer

# Leer un archivo drawio
file = DrawioReader.read_file("ejemplo.drawio")
page = file.pages[0]

# Crear un renderer
renderer = DiagramRenderer()

# Renderizar a SVG
renderer.save_page_as_svg(page, "diagrama.svg")

# Renderizar a HTML interactivo
renderer.save_page_as_html(page, "diagrama.html")
```

### Módulo Writer

El módulo writer proporciona funcionalidad para escribir objetos drawpyo a archivos drawio. Está compuesto por:

- **DrawioWriter**: Clase principal para escribir archivos drawio
- **PythonToXmlConverter**: Convierte objetos drawpyo a elementos XML

#### Uso Básico del Writer

```python
from drawpyo.reader import DrawioReader
from drawpyo.writer import DrawioWriter

# Leer un archivo drawio
file = DrawioReader.read_file("ejemplo.drawio")

# Modificar el diagrama
# ...

# Escribir el diagrama modificado
writer = DrawioWriter()
writer.write_file(file, "modificado.drawio")
```

## Flujo de Trabajo Completo

El siguiente ejemplo muestra un flujo de trabajo completo utilizando todas las extensiones:

```python
from drawpyo.file import File
from drawpyo.page import Page
from drawpyo.diagram.objects import Object
from drawpyo.diagram.edges import Edge
from drawpyo.reader import DrawioReader
from drawpyo.renderer import DiagramRenderer
from drawpyo.writer import DrawioWriter

# 1. Crear un diagrama desde cero
file = File()
page = Page("Mi Diagrama")
file.add_page(page)

# Añadir objetos
rect1 = Object(value="Inicio")
rect1.position = (100, 100)
rect1.width = 120
rect1.height = 60
rect1.apply_style_string("shape=rectangle;fillColor=#d5e8d4;strokeColor=#82b366;rounded=1;")
page.add_object(rect1)

rect2 = Object(value="Proceso")
rect2.position = (300, 100)
rect2.width = 120
rect2.height = 60
rect2.apply_style_string("shape=rectangle;fillColor=#dae8fc;strokeColor=#6c8ebf;")
page.add_object(rect2)

# Añadir un conector
edge = Edge(source=rect1, target=rect2, label="Siguiente")
edge.apply_style_string("edgeStyle=orthogonalEdgeStyle;rounded=0;")
page.add_object(edge)

# 2. Guardar el diagrama
writer = DrawioWriter()
writer.write_file(file, "nuevo_diagrama.drawio")

# 3. Leer un diagrama existente
file2 = DrawioReader.read_file("nuevo_diagrama.drawio")

# 4. Renderizar el diagrama
renderer = DiagramRenderer()
renderer.save_page_as_svg(file2.pages[0], "diagrama.svg")
renderer.save_page_as_html(file2.pages[0], "diagrama.html")
```

## Detalles del Formato Drawio

### Estructura General

Los archivos drawio son archivos XML con la siguiente estructura:

```xml
<mxfile>
  <diagram id="..." name="...">
    <!-- Contenido del diagrama (puede estar comprimido) -->
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- Objetos y conectores -->
        <mxCell id="2" ... />
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### Elementos Principales

- **mxfile**: Elemento raíz del archivo
- **diagram**: Representa una página del diagrama
- **mxGraphModel**: Modelo del diagrama
- **mxCell**: Representa un objeto o conector
- **mxGeometry**: Define la geometría de un objeto o conector

### Atributos Comunes de mxCell

- **id**: Identificador único
- **parent**: ID del padre (generalmente "1" para objetos de nivel superior)
- **vertex**: "1" para formas, "0" o ausente para conectores
- **edge**: "1" para conectores
- **value**: Texto del objeto
- **style**: Cadena de estilo con formato "clave=valor;clave=valor;..."
- **source**: ID del objeto origen (para conectores)
- **target**: ID del objeto destino (para conectores)

### Estilos

Los estilos se definen como cadenas con pares clave-valor separados por punto y coma:

```
shape=rectangle;fillColor=#f5f5f5;strokeColor=#666666;rounded=1;
```

Algunos estilos comunes:
- **shape**: Forma del objeto (rectangle, ellipse, rhombus, etc.)
- **fillColor**: Color de relleno
- **strokeColor**: Color de borde
- **fontColor**: Color de texto
- **rounded**: "1" para esquinas redondeadas
- **edgeStyle**: Estilo de conector (orthogonalEdgeStyle, elbowEdgeStyle, etc.)
- **startArrow**: Tipo de flecha al inicio
- **endArrow**: Tipo de flecha al final

## Tipos de Formas Soportados

Las extensiones soportan los siguientes tipos de formas:

- **rectangle**: Rectángulo
- **ellipse**: Elipse/Círculo
- **rhombus**: Rombo
- **triangle**: Triángulo
- **hexagon**: Hexágono
- **cylinder**: Cilindro
- **cloud**: Nube

## Tipos de Conectores Soportados

Las extensiones soportan los siguientes tipos de conectores:

- **orthogonalEdgeStyle**: Conectores con ángulos rectos
- **elbowEdgeStyle**: Conectores con un solo doblez
- **entityRelationEdgeStyle**: Conectores para diagramas ER
- **segmentEdgeStyle**: Conectores con segmentos rectos
- **straightEdgeStyle**: Conectores en línea recta

## Tipos de Flechas Soportados

Las extensiones soportan los siguientes tipos de flechas:

- **classic**: Flecha triangular clásica
- **block**: Flecha rectangular
- **open**: Flecha en forma de V abierta
- **oval**: Flecha circular
- **diamond**: Flecha en forma de diamante

## Limitaciones Actuales

- No se soportan todas las formas personalizadas de drawio
- No se soportan todas las opciones de formato de texto avanzado
- No se soportan capas múltiples
- No se soportan algunos efectos visuales avanzados

## Ejemplos Adicionales

### Crear un Diagrama de Flujo Simple

```python
from drawpyo.file import File
from drawpyo.page import Page
from drawpyo.diagram.objects import Object
from drawpyo.diagram.edges import Edge
from drawpyo.writer import DrawioWriter

# Crear archivo y página
file = File()
page = Page("Diagrama de Flujo")
file.add_page(page)

# Crear objetos
start = Object(value="Inicio")
start.position = (100, 50)
start.width = 100
start.height = 40
start.apply_style_string("shape=ellipse;fillColor=#d5e8d4;strokeColor=#82b366;")
page.add_object(start)

process1 = Object(value="Proceso 1")
process1.position = (100, 150)
process1.width = 100
process1.height = 60
process1.apply_style_string("shape=rectangle;fillColor=#dae8fc;strokeColor=#6c8ebf;")
page.add_object(process1)

decision = Object(value="¿Condición?")
decision.position = (100, 270)
decision.width = 100
decision.height = 80
decision.apply_style_string("shape=rhombus;fillColor=#fff2cc;strokeColor=#d6b656;")
page.add_object(decision)

process2 = Object(value="Proceso 2")
process2.position = (250, 280)
process2.width = 100
process2.height = 60
process2.apply_style_string("shape=rectangle;fillColor=#dae8fc;strokeColor=#6c8ebf;")
page.add_object(process2)

end = Object(value="Fin")
end.position = (100, 400)
end.width = 100
end.height = 40
end.apply_style_string("shape=ellipse;fillColor=#f8cecc;strokeColor=#b85450;")
page.add_object(end)

# Crear conectores
edge1 = Edge(source=start, target=process1)
edge1.apply_style_string("edgeStyle=orthogonalEdgeStyle;rounded=0;")
page.add_object(edge1)

edge2 = Edge(source=process1, target=decision)
edge2.apply_style_string("edgeStyle=orthogonalEdgeStyle;rounded=0;")
page.add_object(edge2)

edge3 = Edge(source=decision, target=process2, label="Sí")
edge3.apply_style_string("edgeStyle=orthogonalEdgeStyle;rounded=0;")
page.add_object(edge3)

edge4 = Edge(source=decision, target=end, label="No")
edge4.apply_style_string("edgeStyle=orthogonalEdgeStyle;rounded=0;")
page.add_object(edge4)

edge5 = Edge(source=process2, target=end)
edge5.apply_style_string("edgeStyle=orthogonalEdgeStyle;rounded=0;")
page.add_object(edge5)

# Guardar el diagrama
writer = DrawioWriter()
writer.write_file(file, "diagrama_flujo.drawio")
```

### Leer y Modificar un Diagrama Existente

```python
from drawpyo.reader import DrawioReader
from drawpyo.diagram.objects import Object
from drawpyo.diagram.edges import Edge
from drawpyo.writer import DrawioWriter
from drawpyo.renderer import DiagramRenderer

# Leer un diagrama existente
file = DrawioReader.read_file("diagrama_flujo.drawio")
page = file.pages[0]

# Añadir un nuevo objeto
new_obj = Object(value="Nuevo Proceso")
new_obj.position = (400, 150)
new_obj.width = 120
new_obj.height = 60
new_obj.apply_style_string("shape=cloud;fillColor=#e1d5e7;strokeColor=#9673a6;")
page.add_object(new_obj)

# Encontrar un objeto existente por su valor
target_obj = None
for obj in page.objects:
    if isinstance(obj, Object) and not isinstance(obj, Edge):
        if hasattr(obj, 'value') and obj.value == "Proceso 2":
            target_obj = obj
            break

# Conectar el nuevo objeto con uno existente
if target_obj:
    new_edge = Edge(source=new_obj, target=target_obj, label="Conecta")
    new_edge.apply_style_string("edgeStyle=orthogonalEdgeStyle;rounded=0;")
    page.add_object(new_edge)

# Guardar el diagrama modificado
writer = DrawioWriter()
writer.write_file(file, "diagrama_modificado.drawio")

# Renderizar el diagrama
renderer = DiagramRenderer()
renderer.save_page_as_svg(page, "diagrama_modificado.svg")
renderer.save_page_as_html(page, "diagrama_modificado.html")
```

## Conclusión

Las extensiones implementadas para drawpyo proporcionan una solución completa para trabajar con archivos drawio desde Python. Con estas extensiones, es posible leer, representar, modificar y escribir diagramas drawio de manera programática, sin necesidad de utilizar la interfaz gráfica de draw.io.

Estas capacidades abren nuevas posibilidades para la generación automática de diagramas, la modificación por lotes de diagramas existentes, y la integración de diagramas en flujos de trabajo automatizados.
