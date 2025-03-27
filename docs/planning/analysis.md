# Análisis de capacidades actuales de drawpyo

## Estructura general del proyecto

Después de analizar el código fuente de drawpyo, he identificado la siguiente estructura:

### Clases principales
- `XMLBase`: Clase base para todos los objetos exportables en drawpyo
- `DiagramBase`: Clase base para todos los objetos de diagrama
- `File`: Representa un archivo .drawio
- `Page`: Representa una página dentro de un archivo .drawio
- `Object`: Clase base para todas las formas en Draw.io
- `BasicObject`: Versión simplificada de Object
- `Group`: Permite agrupar objetos
- `Edge`: Clase para definir bordes o flechas
- `BasicEdge`: Versión simplificada de Edge
- `Geometry`: Define la geometría de un objeto
- `EdgeGeometry`: Almacena la geometría asociada a un borde
- `Point`: Representa un punto en el diagrama
- `TextFormat`: Maneja el formato de texto

### Bibliotecas de formas
- `general.toml`: Formas generales
- `flowchart.toml`: Formas de diagrama de flujo
- `line_styles.toml`: Estilos de línea
- `edge_styles.toml`: Estilos de bordes

## Capacidades actuales

### Generación de diagramas
- Creación de archivos .drawio
- Soporte para múltiples páginas
- Creación de formas básicas
- Creación de conectores (edges)
- Agrupación de objetos
- Aplicación de estilos básicos

### Tipos de objetos soportados
- Formas básicas (rectángulos, elipses, etc.)
- Formas de diagrama de flujo
- Conectores simples y con flechas
- Grupos de objetos

### Estilos soportados
- Colores de relleno y borde
- Estilos de línea (sólido, punteado, etc.)
- Formato de texto básico
- Sombras, bordes redondeados
- Opacidad
- Animación de flujo

## Limitaciones identificadas

### Tipos de objetos
1. **Falta soporte para formas avanzadas**:
   - Formas UML
   - Formas de red
   - Formas de AWS, Azure, GCP
   - Formas de BPMN
   - Formas de ER
   - Formas de circuitos

2. **Falta soporte para elementos complejos**:
   - Tablas
   - Imágenes
   - Contenedores complejos
   - Swimlanes
   - Formas personalizadas

### Funcionalidades
1. **No hay soporte para lectura de archivos .drawio**:
   - No puede parsear archivos .drawio existentes
   - No maneja contenido comprimido en base64

2. **Limitaciones en conectores**:
   - Opciones limitadas para puntos de conexión
   - Falta soporte para conectores curvos avanzados
   - No hay soporte para etiquetas múltiples en conectores

3. **Limitaciones en estilos**:
   - Falta soporte para gradientes
   - Falta soporte para patrones de relleno
   - Opciones limitadas para estilos de texto

## Puntos de extensión identificados

1. **Ampliación de bibliotecas de formas**:
   - Añadir nuevas bibliotecas TOML para tipos de formas adicionales
   - Extender las bibliotecas existentes con más opciones

2. **Implementación de lectura de archivos**:
   - Añadir funcionalidad para parsear XML de archivos .drawio
   - Implementar descompresión de contenido en base64

3. **Extensión de clases existentes**:
   - Ampliar `Object` para soportar más tipos de formas
   - Ampliar `Edge` para soportar más tipos de conectores
   - Añadir nuevas clases para elementos complejos

4. **Mejora de estilos**:
   - Ampliar las opciones de estilo en las clases existentes
   - Implementar soporte para gradientes y patrones

## Próximos pasos

1. Crear un fork del repositorio
2. Identificar en detalle los elementos específicos de drawio que faltan por implementar
3. Diseñar las ampliaciones necesarias
4. Implementar las nuevas funcionalidades con commits frecuentes
5. Probar la implementación
6. Documentar los cambios
