# Implementación de la funcionalidad de lectura de archivos drawio

Comenzaremos implementando la funcionalidad para leer archivos drawio existentes, que es una de las principales limitaciones identificadas en el análisis.

## Estructura de archivos

Crearemos un nuevo módulo `reader` con los siguientes archivos:
- `__init__.py`: Exporta las clases principales
- `parser.py`: Contiene la lógica para parsear archivos XML de drawio
- `decompressor.py`: Maneja la descompresión de contenido en base64+deflate
- `converter.py`: Convierte elementos XML a objetos drawpyo

## Implementación

Primero implementaremos el descompresor para manejar el contenido comprimido en los archivos drawio.
