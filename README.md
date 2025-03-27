# Drawpyo Extensions - README

Este proyecto extiende la biblioteca [drawpyo](https://github.com/MerrimanInd/drawpyo) para proporcionar soporte completo para el formato drawio, permitiendo leer, representar, modificar y escribir archivos drawio desde Python.

## Características Principales

- **Lectura de archivos drawio**: Parseo completo de archivos drawio, incluyendo soporte para contenido comprimido en base64+deflate
- **Representación visual**: Renderizado de diagramas en formatos SVG y HTML interactivo
- **Modificación programática**: API para modificar diagramas existentes o crear nuevos desde cero
- **Escritura de archivos drawio**: Conversión de objetos drawpyo a archivos drawio compatibles

## Estructura del Proyecto

- **src/drawpyo/reader/**: Módulo para leer y parsear archivos drawio
- **src/drawpyo/renderer/**: Módulo para renderizar diagramas en formatos visuales
- **src/drawpyo/writer/**: Módulo para escribir diagramas a archivos drawio
- **examples/**: Scripts de ejemplo que demuestran el uso de las extensiones
- **docs/**: Documentación detallada sobre las extensiones

## Ejemplo Rápido

```python
from drawpyo.file import File
from drawpyo.page import Page
from drawpyo.diagram.objects import Object
from drawpyo.diagram.edges import Edge
from drawpyo.reader import DrawioReader
from drawpyo.renderer import DiagramRenderer
from drawpyo.writer import DrawioWriter

# Leer un archivo drawio existente
file = DrawioReader.read_file("ejemplo.drawio")

# Modificar el diagrama
page = file.pages[0]
new_obj = Object(value="Nuevo Objeto")
new_obj.position = (300, 200)
new_obj.width = 120
new_obj.height = 60
new_obj.apply_style_string("shape=rectangle;fillColor=#d5e8d4;strokeColor=#82b366;")
page.add_object(new_obj)

# Guardar el diagrama modificado
writer = DrawioWriter()
writer.write_file(file, "modificado.drawio")

# Renderizar el diagrama
renderer = DiagramRenderer()
renderer.save_page_as_svg(page, "diagrama.svg")
renderer.save_page_as_html(page, "diagrama.html")
```

## Documentación

Para una documentación completa, consulte [DOCUMENTATION.md](docs/DOCUMENTATION.md).

## Limitaciones Actuales

- No se soportan todas las formas personalizadas de drawio
- No se soportan todas las opciones de formato de texto avanzado
- No se soportan capas múltiples
- No se soportan algunos efectos visuales avanzados

## Contribuciones

Las contribuciones son bienvenidas. Por favor, siéntase libre de abrir issues o pull requests para mejorar este proyecto.

## Licencia

Este proyecto se distribuye bajo la misma licencia que drawpyo original.
