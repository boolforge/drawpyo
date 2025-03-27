# Estudio en profundidad del formato drawio

Para entender completamente el formato drawio, necesitamos analizar su estructura XML, los elementos que lo componen, y cómo se relacionan entre sí. Este documento recopila información detallada sobre el formato basada en el análisis de archivos de ejemplo y la documentación disponible.

## Estructura general de un archivo .drawio

Un archivo .drawio es un documento XML con la siguiente estructura jerárquica:

```xml
<mxfile>
  <diagram id="..." name="...">
    <!-- Contenido del diagrama (puede estar comprimido) -->
  </diagram>
  <!-- Posibles diagramas adicionales -->
</mxfile>
```

### Elemento raíz: `<mxfile>`

El elemento raíz de un archivo .drawio es `<mxfile>`, que contiene los siguientes atributos:

- `host`: La aplicación que generó el archivo (ej. "app.diagrams.net")
- `modified`: Fecha y hora de la última modificación (formato ISO)
- `agent`: Información sobre el agente que creó el archivo (navegador, versión)
- `etag`: Identificador único para control de versiones
- `version`: Versión del formato (ej. "21.6.5")
- `type`: Tipo de archivo (ej. "device", "google", "onedrive")

### Elemento `<diagram>`

Cada página del diagrama se representa con un elemento `<diagram>` que tiene estos atributos:

- `id`: Identificador único del diagrama
- `name`: Nombre visible de la página

El contenido del diagrama puede estar:
1. Directamente como XML dentro del elemento `<diagram>`
2. Como texto comprimido en base64+deflate

## Contenido del diagrama

Cuando se descomprime (si es necesario), el contenido del diagrama tiene esta estructura:

```xml
<mxGraphModel>
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <!-- Elementos del diagrama -->
  </root>
</mxGraphModel>
```

### Elemento `<mxGraphModel>`

Este elemento representa el modelo del diagrama y puede tener estos atributos:

- `dx`: Desplazamiento horizontal del origen
- `dy`: Desplazamiento vertical del origen
- `grid`: Si la cuadrícula está visible (0 o 1)
- `gridSize`: Tamaño de la cuadrícula en píxeles
- `guides`: Si las guías están habilitadas (0 o 1)
- `tooltips`: Si los tooltips están habilitados (0 o 1)
- `connect`: Si la conexión está habilitada (0 o 1)
- `arrows`: Si las flechas están habilitadas (0 o 1)
- `fold`: Si el plegado está habilitado (0 o 1)
- `page`: Si se muestra como página (0 o 1)
- `pageScale`: Escala de la página
- `pageWidth`: Ancho de la página en píxeles
- `pageHeight`: Alto de la página en píxeles
- `background`: Color de fondo (ej. "#ffffff")

### Elemento `<root>`

Contiene todos los elementos del diagrama. Siempre incluye dos celdas especiales:

1. `<mxCell id="0"/>`: Celda raíz
2. `<mxCell id="1" parent="0"/>`: Capa predeterminada (todos los elementos visibles son hijos de esta celda)

### Elemento `<mxCell>`

Cada elemento del diagrama (formas, conectores, grupos) se representa como un `<mxCell>` con estos atributos:

- `id`: Identificador único de la celda
- `parent`: ID de la celda padre (generalmente "1" para elementos de nivel superior)
- `value`: Texto o contenido HTML asociado con la celda
- `style`: Cadena de estilo que define la apariencia (formato clave=valor separado por punto y coma)
- `vertex`: "1" para formas, no presente o "0" para conectores
- `edge`: "1" para conectores, no presente para formas
- `source`: Para conectores, ID de la celda de origen
- `target`: Para conectores, ID de la celda de destino

### Elemento `<mxGeometry>`

Define la geometría de una celda y puede ser un elemento hijo de `<mxCell>`:

```xml
<mxCell id="...">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>
```

Atributos comunes:

- `x`: Coordenada X en píxeles
- `y`: Coordenada Y en píxeles
- `width`: Ancho en píxeles
- `height`: Alto en píxeles
- `as`: Generalmente "geometry"
- `relative`: "1" para geometría relativa (común en conectores)

Para conectores, puede contener puntos adicionales:

```xml
<mxCell id="..." edge="1" source="..." target="...">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="200" y="150" as="sourcePoint"/>
    <mxPoint x="300" y="150" as="targetPoint"/>
    <Array as="points">
      <mxPoint x="250" y="200"/>
    </Array>
  </mxGeometry>
</mxCell>
```

## Estilos

El atributo `style` de un `<mxCell>` define su apariencia visual. Es una cadena con formato clave=valor separado por punto y coma:

```
shape=rectangle;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;
```

### Estilos comunes para formas (vertex)

- `shape`: Tipo de forma (rectangle, ellipse, rhombus, etc.)
- `whiteSpace`: Manejo de espacios en blanco (wrap, nowrap)
- `html`: Si el valor se interpreta como HTML (0 o 1)
- `rounded`: Si los bordes son redondeados (0 o 1)
- `fillColor`: Color de relleno (código hexadecimal)
- `strokeColor`: Color de borde (código hexadecimal)
- `fontColor`: Color de texto (código hexadecimal)
- `fontSize`: Tamaño de fuente en puntos
- `fontFamily`: Familia de fuente
- `fontStyle`: Estilo de fuente (0=normal, 1=negrita, 2=cursiva, 3=negrita+cursiva)
- `opacity`: Opacidad (0-100)
- `shadow`: Si tiene sombra (0 o 1)
- `dashed`: Si el borde es discontinuo (0 o 1)
- `dashPattern`: Patrón de línea discontinua
- `strokeWidth`: Ancho del borde en píxeles
- `align`: Alineación horizontal del texto (left, center, right)
- `verticalAlign`: Alineación vertical del texto (top, middle, bottom)
- `spacingLeft`, `spacingRight`, `spacingTop`, `spacingBottom`: Espaciado interno

### Estilos comunes para conectores (edge)

- `edgeStyle`: Estilo del conector (orthogonalEdgeStyle, elbowEdgeStyle, etc.)
- `curved`: Si el conector es curvo (0 o 1)
- `rounded`: Si las esquinas son redondeadas (0 o 1)
- `entryX`, `entryY`: Punto de entrada en la celda destino (0-1)
- `exitX`, `exitY`: Punto de salida en la celda origen (0-1)
- `entryDx`, `entryDy`: Desplazamiento del punto de entrada
- `exitDx`, `exitDy`: Desplazamiento del punto de salida
- `endArrow`: Tipo de flecha en el extremo (classic, block, open, etc.)
- `startArrow`: Tipo de flecha en el inicio
- `endFill`: Si la flecha del extremo está rellena (0 o 1)
- `startFill`: Si la flecha del inicio está rellena (0 o 1)
- `endSize`: Tamaño de la flecha del extremo
- `startSize`: Tamaño de la flecha del inicio
- `jumpStyle`: Estilo de salto en cruces (arc, gap, sharp)
- `jumpSize`: Tamaño del salto

## Formas especiales

### Swimlanes

```xml
<mxCell id="..." value="Swimlane" style="swimlane;..." vertex="1">
  <mxGeometry x="100" y="100" width="200" height="200" as="geometry"/>
</mxCell>
```

### Tablas

```xml
<mxCell id="..." value="&lt;table&gt;...&lt;/table&gt;" style="shape=table;..." vertex="1">
  <mxGeometry x="100" y="100" width="200" height="200" as="geometry"/>
</mxCell>
```

### Imágenes

```xml
<mxCell id="..." value="" style="shape=image;imageAspect=0;aspect=fixed;image=data:image/png,base64,..." vertex="1">
  <mxGeometry x="100" y="100" width="200" height="200" as="geometry"/>
</mxCell>
```

## Grupos

Los grupos se crean estableciendo el `parent` de las celdas al ID de la celda del grupo:

```xml
<mxCell id="group1" value="Group" style="group" vertex="1" connectable="0">
  <mxGeometry x="100" y="100" width="200" height="200" as="geometry"/>
</mxCell>
<mxCell id="rect1" value="Rectangle" style="rectangle" vertex="1" parent="group1">
  <mxGeometry x="10" y="10" width="80" height="40" as="geometry"/>
</mxCell>
```

## Capas

Las capas son similares a los grupos pero con propiedades especiales:

```xml
<mxCell id="layer2" value="Layer 2" style="layer" parent="0"/>
<mxCell id="rect2" value="Rectangle in Layer 2" style="rectangle" vertex="1" parent="layer2">
  <mxGeometry x="100" y="100" width="80" height="40" as="geometry"/>
</mxCell>
```

## Compresión

El contenido del diagrama puede estar comprimido en base64+deflate:

1. El contenido XML se comprime usando el algoritmo deflate (zlib sin cabecera)
2. El resultado se codifica en base64
3. Esta cadena se coloca como contenido del elemento `<diagram>`

Para descomprimir:
1. Decodificar la cadena base64
2. Descomprimir usando zlib con `-zlib.MAX_WBITS` para indicar que no hay cabecera

## Consideraciones adicionales

### Elementos UserObject

Para elementos con etiquetas:

```xml
<UserObject label="Label" tags="tag1,tag2" id="cell1">
  <mxCell style="..." vertex="1">
    <mxGeometry x="100" y="100" width="80" height="40" as="geometry"/>
  </mxCell>
</UserObject>
```

### Bibliotecas personalizadas

Las bibliotecas de formas personalizadas se almacenan en elementos `<mxlibrary>` que contienen datos JSON codificados en base64.

### Metadatos

Los metadatos adicionales pueden almacenarse en elementos `<mxMetadata>`.

## Conclusión

El formato drawio es un formato XML estructurado con una jerarquía clara de elementos. Cada elemento del diagrama se representa como un `<mxCell>` con atributos específicos y un elemento `<mxGeometry>` que define su posición y tamaño. Los estilos se definen mediante cadenas de texto con pares clave-valor. El contenido puede estar comprimido en base64+deflate para reducir el tamaño del archivo.

Esta documentación proporciona una base sólida para implementar un parser completo que pueda leer, representar, modificar y escribir archivos drawio.
