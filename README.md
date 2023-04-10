# Altium Schematic Document Parser #

Python API to read and parse Altium schematic documents.

## Usage
```
s = schdoc.Schematic("<path-to-.SchDoc>")
s.read()
```

## API
### Schematics
 - `path`: File path to schematic document
 - `records`: All parsed records in the document 
 - `files`: All files in document (currently only supporting images)
 - `name`: Name of the schematic
### Record Types
#### ComponentRecord
 - Record ID: 1
 - library_reference
 - design_item_id
 - description
 - current_part_id
 - display_mode
 - part_count

#### PinRecord
 - Record ID: 2
 - x
 - y
 - length
 - owner_display_mode
 - orientation
 - angle
 - name
 - show_name
 - designator
 - show_designator
 - angle_vec
 - name_orientation

#### IEEESymbolRecord
 - Record ID: 3

#### LabelRecord
 - Record ID: 4
 - x
 - y
 - text
 - hidden
 - color
 - orientation
 - justification
 - font_id

#### BezierRecord
 - Record ID: 5

#### PolylineRecord
 - Record ID: 6
 - points
 - width
 - color
 - start_shape
 - end_shape
 - shape_size
 - line_style

#### PolygonRecord
 - Record ID: 7
 - points
 - width
 - line_color
 - fill_color

#### EllipseRecord
 - Record ID: 8
 - x
 - y
 - radius_x
     - radius_y
     - radius_y
 - width
 - line_color
 - fill_color
 - transparent

#### PiechartRecord
 - Record ID: 9

#### RoundedRectangleRecord
 - Record ID: 10

#### EllipticalArcRecord
 - Record ID: 11
 - x
 - y
 - radius
 - secondary_radius
 - start_angle
 - end_angle
 - width
 - color

#### ArcRecord
 - Record ID: 12
 - x
 - y
 - radius
 - start_angle
 - end_angle
 - width
 - color

#### LineRecord
 - Record ID: 13
 - x1
 - x2
 - y1
 - y2
 - width
 - color

#### RectangleRecord
 - Record ID: 14
 - left
 - right
 - top
 - bottom
 - line_color
 - fill_color
 - owner_display_mode
 - transparent

#### SheetSymbolRecord
 - Record ID: 15
 - x
 - y
 - width
 - height
 - fill_color
 - line_color

#### SheetEntryRecord
 - Record ID: 16
 - from_top
 - iotype
 - font_id
 - side
 - style
 - color
 - text_color
 - fill_color
 - name
 - type

#### PowerPortRecord
 - Record ID: 17
 - x
 - y
 - color
 - show_text
 - text
 - style
 - justification
 - is_off_sheet_connector

#### PortRecord
 - Record ID: 18 - x
 - y
 - width
 - height
 - border_color
 - fill_color
 - color
 - text
 - iotype
 - orientation

#### NoERCRecord
 - Record ID: 22 - x
 - y
 - color
 - orientation
 - symbol

#### NetLabelRecord
 - Record ID: 25
 - x
 - y
 - color
 - text
 - orientation
 - justification
 - font_id

#### BusRecord
 - Record ID: 26 - points
 - color
 - width

#### WireRecord
 - Record ID: 27
 - points
 - color

#### TextFrameRecord
 - Record ID: 28 - left
 - bottom
 - right
 - top
 - border_color
 - text_color
 - fill_color
 - text
 - orientation
 - alignment
 - show_border
 - transparent
 - text_margin
 - word_wrap
 - font_id

#### JunctionRecord
 - Record ID: 29
 - x
 - y
 - color

#### ImageRecord
 - Record ID: 30
 - x
 - y
 - corner_x
 - corner_y
 - corner_x_frac
 - corner_y_frac
 - keep_aspect
 - embedded
 - filename

#### SheetRecord
 - Record ID: 31    SHEET_SIZES = [
    ] - grid_size
 - show_grid
 - areacolor     - width
     - height
     - width
     - height - fonts
     - fonts[f]

#### SheetNameRecord
 - Record ID: 32
 - x
 - y
 - color
 - text
 - font_id

#### SheetFilenameRecord
 - Record ID: 33
 - x
 - y
 - color
 - text
 - font_id

#### DesignatorRecord
 - Record ID: 34
 - x
 - y
 - color
 - hidden
 - text
 - mirrored
 - orientation
 - font_id
 - owner_display_mode    def get_refdes(self):

#### TemplateFileRecord
 - Record ID: 39

#### ParameterRecord
 - Record ID: 41
 - x
 - y
 - color
 - name
 - text
 - hidden
 - mirrored
 - orientation
 - font_id
 - owner_display_mode

#### WarningSignRecord
 - Record ID: 43

#### ImplementationListRecord
 - Record ID: 44

#### ImplementationRecord
 - Record ID: 45
 - iscurrent
 - description
 - modelname
 - model_type

#### ImplementationPinAssociationRecord
 - Record ID: 46

#### ImplementationPinRecord
 - Record ID: 47
 - pin_name

#### ImplementationParameterListRecord
 - Record ID: 48

## References

https://github.com/esophagoose/python-altium/blob/master/format.md

