# Tags

## Tags in Draw.io

Draw.io supports a function called Tags for hiding or showing groups of objects. To open the tags dialog select it from the View menu.

## Tags in drawpyo

Tags can be added to any drawpyo object or edge by setting its `tag` parameter.

```
object = drawpyo.diagram.Object(page=page, rounded=1)
object.tag = "Tag 1"
```

In Draw.io when the object at either end of an edge gets a tag, the edge also gets the tag. A tag can additionally be applied specifically to the edge. Drawpyo doesn't apply tags like this automatically so the tag would have to be applied to the connected edges manually.