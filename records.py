from enum import Enum


class Record:
    def __init__(self, parameters):
        self.parameters = {}
        for name, value in parameters.items():
            normalized_name = name.lower().replace("%", "_")
            normalized_name = normalized_name.replace(".", "_").replace("_utf8_", "")
            self.parameters[normalized_name] = value

        self.ownerindex = self.get("ownerindex", int)
        self.indexinsheet = self.get("indexinsheet", int)
        self.ownerpartid = self.get("ownerpartid", int)
        self.ownerpartdisplaymode = self.get("ownerpartdisplaymode", int)
        self.parent = None
        self.children = []

    def get(self, name, type=str, default_value=None):
        value = self.parameters.get(name, default_value)
        return type(value) if value else value


class ComponentRecord(Record):
    RECORD_ID = 1

    def __init__(self, record):
        super().__init__(record)
        self.library_reference = self.get("libreference")
        self.design_item_id = self.get("designitemid")
        self.description = self.get("componentdescription", str, "")
        self.current_part_id = self.get("currentpartid", int)
        self.display_mode = self.get("displaymode", int)
        self.part_count = self.get("partcount", int, 1)


class PinRecord(Record):
    RECORD_ID = 2

    def __init__(self, record):
        super().__init__(record)
        self.x = self.get("location_x", int)
        self.y = self.get("location_y", int)
        self.length = self.get("pinlength", int)
        self.owner_display_mode = self.get("ownerpartdisplaymode", int)
        conglomerate = self.get("pinconglomerate", int)
        self.orientation = conglomerate & 3
        self.angle = 90 * self.orientation
        self.name = self.get("name", str, "")
        self.show_name = (conglomerate & 0x8) == 0x8
        self.designator = self.get("designator") or ""
        self.show_designator = (conglomerate & 0x10) == 0x10
        angle_vec_table = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        self.angle_vec = angle_vec_table[self.orientation]
        self.name_orientation = self.get("pinname_positionconglomerate", int, 0)


class IEEESymbolRecord(Record):
    RECORD_ID = 3

    def __init__(self, record):
        super().__init__(record)


class LabelRecord(Record):
    RECORD_ID = 4

    def __init__(self, record):
        super().__init__(record)
        self.x = self.get("location_x", int)
        self.y = self.get("location_y", int)
        self.text = self.get("text")
        self.hidden = self.get("ishidden", str, "") == "T"
        self.color = parse_color(self.get("color"))
        self.orientation = self.get("orientation", int, 0)
        self.justification = self.get("justification", int, 0)
        self.font_id = self.get("fontid", int)


class BezierRecord(Record):
    RECORD_ID = 5

    def __init__(self, record):
        super().__init__(record)


class PolylineRecord(Record):
    RECORD_ID = 6

    def __init__(self, record):
        super().__init__(record)
        self.points = []
        idx = 1
        while self.get(f"x{idx}"):
            x = self.get(f"x{idx}", int)
            y = self.get(f"y{idx}", int)
            self.points.append([x, y])
            idx += 1
        self.width = self.get("linewidth", int, 0)
        self.color = parse_color(self.get("color"))
        self.start_shape = self.get("startlineshape", int, 0)
        self.end_shape = self.get("endlineshape", int, 0)
        self.shape_size = self.get("lineshapesize", int, 0)
        self.line_style = LineStyle(self.get("linestyle", int, 0))


class PolygonRecord(Record):
    RECORD_ID = 7

    def __init__(self, record):
        super().__init__(record)
        self.points = []
        idx = 1
        while self.get(f"x{idx}"):
            x = self.get(f"x{idx}", int)
            y = self.get(f"y{idx}", int)
            self.points.append({x: x, y: y})
            idx += 1
        self.width = self.get("linewidth", int, 0)
        self.line_color = parse_color(self.get("color"))
        self.fill_color = parse_color(self.get("areacolor"))


class EllipseRecord(Record):
    RECORD_ID = 8

    def __init__(self, record):
        super().__init__(record)
        self.x = self.get("location_x", int)
        self.y = self.get("location_y", int)
        self.radius_x = self.get("radius", int)
        if self.get("secondaryradius"):
            self.radius_y = self.get("secondaryradius", int)
        else:
            self.radius_y = self.radius_x
        self.width = self.get("linewidth", int, 1)
        self.line_color = parse_color(self.get("color"))
        self.fill_color = parse_color(self.get("areacolor"))
        self.transparent = self.get("issolid", str, "") != "T"


class PiechartRecord(Record):
    RECORD_ID = 9

    def __init__(self, record):
        super().__init__(record)


class RoundedRectangleRecord(Record):
    RECORD_ID = 10

    def __init__(self, record):
        super().__init__(record)


class EllipticalArcRecord(Record):
    RECORD_ID = 11

    def __init__(self, record):
        super().__init__(record)
        self.x = self.get("location_x", int)
        self.y = self.get("location_y", int)
        self.radius = self.get("radius", int)
        self.secondary_radius = self.get("secondaryradius", int)
        self.start_angle = float(self.get("startangle") or "0")
        self.end_angle = float(self.get("endangle") or "360")
        self.width = self.get("linewidth", int, 1)
        self.color = parse_color(self.get("color"))


class ArcRecord(Record):
    RECORD_ID = 12

    def __init__(self, record):
        super().__init__(record)
        self.x = self.get("location_x", int)
        self.y = self.get("location_y", int)
        self.radius = self.get("radius", int)
        self.start_angle = float(self.get("startangle") or "0")
        self.end_angle = float(self.get("endangle") or "360")
        self.width = self.get("linewidth", int, 1)
        self.color = parse_color(self.get("color"))


class LineRecord(Record):
    RECORD_ID = 13

    def __init__(self, record):
        super().__init__(record)
        self.x1 = self.get("location_x", int)
        self.x2 = self.get("corner_x", int)
        self.y1 = self.get("corner_y", int)
        self.y2 = self.get("location_y", int)
        self.width = self.get("linewidth", int, 1)
        self.color = parse_color(self.get("color"))


class RectangleRecord(Record):
    RECORD_ID = 14

    def __init__(self, record):
        super().__init__(record)
        self.left = self.get("location_x", int)
        self.right = self.get("corner_x", int)
        self.top = self.get("corner_y", int)
        self.bottom = self.get("location_y", int)
        self.line_color = parse_color(self.get("color"))
        self.fill_color = parse_color(self.get("areacolor"))
        self.owner_display_mode = self.get("ownerpartdisplaymode", int)
        self.transparent = (
            self.get("issolid", str, "F") != "T"
            or self.get("transparent", str, "F") == "T"
            and self.owner_display_mode < 1
        )


class SheetSymbolRecord(Record):
    RECORD_ID = 15

    def __init__(self, record):
        super().__init__(record)
        self.x = self.get("location_x", int)
        self.y = self.get("location_y", int)
        self.width = self.get("xsize", int)
        self.height = self.get("ysize", int)
        self.fill_color = parse_color(self.get("areacolor"))
        self.line_color = parse_color(self.get("color"))


class SheetEntryRecord(Record):
    RECORD_ID = 16

    def __init__(self, record):
        super().__init__(record)
        self.from_top = 10 * self.get("distancefromtop", int)
        self.iotype = self.get("iotype", int)
        self.font_id = self.get("textfontid", int)
        self.side = self.get("side", int, 0)
        self.style = self.get("style", int)
        self.color = parse_color(self.get("color"))
        self.text_color = parse_color(self.get("textcolor"))
        self.fill_color = parse_color(self.get("areacolor"))
        self.name = self.get("name")
        self.type = self.get("arrowkind")


class PowerPortRecord(Record):
    RECORD_ID = 17

    def __init__(self, record):
        super().__init__(record)
        self.x = self.get("location_x", int)
        self.y = self.get("location_y", int)
        self.color = parse_color(self.get("color"))
        self.show_text = self.get("shownetname", str, "") == "T"
        self.text = self.get("text", str, "")
        self.style = Style(self.get("style", int, 0))
        self.justification = self.get("orientation", int, 0)
        self.is_off_sheet_connector = self.get("iscrosssheetconnector", str, "") == "T"


class PortRecord(Record):
    RECORD_ID = 18

    def __init__(self, record):
        super().__init__(record)

        self.x = self.get("location_x", int)
        self.y = self.get("location_y", int)
        self.width = self.get("width", int)
        self.height = self.get("height", int)
        self.border_color = parse_color(self.get("color"))
        self.fill_color = parse_color(self.get("areacolor") or "16777215")
        self.color = parse_color(self.get("textcolor"))
        self.text = self.get("name") or ""
        self.iotype = self.get("iotype", int, 0)
        self.orientation = self.get("style", int, 0) >> 2


class NoERCRecord(Record):
    RECORD_ID = 22

    def __init__(self, record):
        super().__init__(record)

        self.x = self.get("location_x", int)
        self.y = self.get("location_y", int)
        self.color = parse_color(self.get("color"))
        self.orientation = self.get("orientation", int, 0)
        self.symbol = self.get("symbol")


class NetLabelRecord(Record):
    RECORD_ID = 25

    def __init__(self, record):
        super().__init__(record)
        self.x = self.get("location_x", int)
        self.y = self.get("location_y", int)
        self.color = parse_color(self.get("color"))
        self.text = self.get("text", str, "")
        self.orientation = self.get("orientation", int, 0)
        self.justification = self.get("justification", int, 0)
        self.font_id = self.get("font_id", int, 1)


class BusRecord(Record):
    RECORD_ID = 26

    def __init__(self, record):
        super().__init__(record)

        self.points = []
        idx = 1
        while self.get(f"x{idx}"):
            x = self.get(f"x{idx}", int)
            y = self.get(f"y{idx}", int)
            self.points.append({x: x, y: y})
            idx += 1
        self.color = parse_color(self.get("color"))
        self.width = 3 * self.get("linewidth", int)


class WireRecord(Record):
    RECORD_ID = 27

    def __init__(self, record):
        super().__init__(record)
        self.points = []
        idx = 1
        while self.get(f"x{idx}"):
            x = self.get(f"x{idx}", int)
            y = self.get(f"y{idx}", int)
            self.points.append({x: x, y: y})
            idx += 1
        self.color = parse_color(self.get("color"))


class TextFrameRecord(Record):
    RECORD_ID = 28

    def __init__(self, record):
        super().__init__(record)

        self.left = self.get("location_x", int)
        self.bottom = self.get("location_y", int)
        self.right = self.get("corner_x", int)
        self.top = self.get("corner_y", int)
        self.border_color = parse_color(self.get("color"))
        self.text_color = parse_color(self.get("textcolor"))
        self.fill_color = self.get("areacolor", int, "16777215")
        self.text = self.get("text", str, "")
        self.orientation = self.get("orientation", int, 0)
        self.alignment = self.get("alignment", int, 0)
        self.show_border = self.get("showborder", str, "") == "T"
        self.transparent = self.get("issolid", str, "") != "F"
        self.text_margin = self.get("textmargin", int, 2)
        self.word_wrap = self.get("wordwrap", str, "F") == "T"
        self.font_id = self.get("fontid", int)


class JunctionRecord(Record):
    RECORD_ID = 29

    def __init__(self, record):
        super().__init__(record)
        self.x = self.get("location_x", int)
        self.y = self.get("location_y", int)
        self.color = parse_color(self.get("color"))


class ImageRecord(Record):
    RECORD_ID = 30

    def __init__(self, record):
        super().__init__(record)
        self.x = self.get("location_x", int)
        self.y = self.get("location_y", int)
        self.corner_x = self.get("corner_x", int)
        self.corner_y = self.get("corner_y", int)
        self.corner_x_frac = self.get("corner_x_frac", int)
        self.corner_y_frac = self.get("corner_y_frac", int)
        self.keep_aspect = self.get("keepaspect", str, "F") == "T"
        self.embedded = self.get("embedimage", str, "F") == "T"
        self.filename = self.get("filename")


class SheetRecord(Record):
    RECORD_ID = 31

    SHEET_SIZES = [
        [1150, 760],
        [1550, 1110],
        [2230, 1570],
        [3150, 2230],
        [4460, 3150],
        [950, 750],
        [1500, 950],
        [2000, 1500],
        [3200, 2000],
        [4200, 3200],
        [1100, 850],
        [1400, 850],
        [1700, 1100],
        [990, 790],
        [1540, 990],
        [2060, 1560],
        [3260, 2060],
        [4280, 3280],
    ]

    def __init__(self, record):
        super().__init__(record)

        self.grid_size = self.get("visiblegridsize", int, 10)
        self.show_grid = self.get("visiblegridon", str, "") != "F"
        self.areacolor = parse_color(self.get("areacolor"))

        if self.get("usecustomsheet") == "T":
            self.width = self.get("customx", int)
            self.height = self.get("customy", int)
        else:
            paper_size = self.get("sheetstyle", int, 0)
            self.width = SHEET_SIZES[paper_size][0]
            self.height = SHEET_SIZES[paper_size][1]

        f = 1
        self.fonts = {}
        while self.parameters.get(f"fontname{f}"):
            name = self.parameters[f"fontname{f}"]
            size = self.get(f"size{f}", int, 12)
            bold = self.get(f"bold{f}", str, "") == "T"
            italics = self.get(f"italics{f}", str, "") == "T"
            self.fonts[f] = {
                name: name,
                size: size,
                bold: bold,
                italics: bold,
            }
            f += 1


class SheetNameRecord(Record):
    RECORD_ID = 32

    def __init__(self, record):
        super().__init__(record)
        self.x = self.get("location_x", int, 0)
        self.y = self.get("location_y", int, 0)
        self.color = parse_color(self.get("color"))
        self.text = self.get("text", str, "")
        self.font_id = self.get("fontid", int, 1)


class SheetFilenameRecord(Record):
    RECORD_ID = 33

    def __init__(self, record):
        super().__init__(record)
        self.x = self.get("location_x", int, 0)
        self.y = self.get("location_y", int, 0)
        self.color = parse_color(self.get("color"))
        self.text = self.get("text", str, "")
        self.font_id = self.get("fontid", int, 1)


class DesignatorRecord(Record):
    RECORD_ID = 34

    def __init__(self, record):
        super().__init__(record)
        self.x = self.get("location_x", int, 0)
        self.y = self.get("location_y", int, 0)
        self.color = parse_color(self.get("color"))
        self.hidden = self.get("ishidden", str, "") == "T"
        self.text = self.get("text", str, "")
        self.mirrored = self.get("ismirrored", str, "") == "T"
        self.orientation = self.get("orientation", int, 0)
        self.font_id = self.get("font_id", int, 1)
        self.owner_display_mode = self.get("ownerpartdisplaymode", int)

    def get_refdes(self):
        if not self.parent:
            return self.text

        if 0 < self.parent.current_part_id <= 26:
            letter = chr(parent.current_part_id + ord("A") - 1)
            return self.text + letter
        else:
            return f"{self.text}[{self.parent.current_part_id}]"
        return self.text


class TemplateFileRecord(Record):
    RECORD_ID = 39

    def __init__(self, record):
        super().__init__(record)


class ParameterRecord(Record):
    RECORD_ID = 41

    def __init__(self, record):
        super().__init__(record)
        self.x = self.get("location_x", int, 0)
        self.y = self.get("location_y", int, 0)
        self.color = parse_color(self.get("color"))
        self.name = self.get("name", str, "")
        self.text = self.get("text", str, "")
        self.hidden = self.get("ishidden", str, "") == "T"
        self.mirrored = self.get("ismirrored", str, "") == "T"
        self.orientation = self.get("orientation", int, 0)
        self.font_id = self.get("font_id", int, 1)
        self.owner_display_mode = self.get("ownerpartdisplaymode", int)


class WarningSignRecord(Record):
    RECORD_ID = 43

    def __init__(self, record):
        super().__init__(record)


class ImplementationListRecord(Record):
    RECORD_ID = 44

    def __init__(self, record):
        super().__init__(record)


class ImplementationRecord(Record):
    RECORD_ID = 45

    def __init__(self, record):
        super().__init__(record)
        self.iscurrent = self.get("iscurrent", str, "") == "T"
        self.description = self.get("description")
        self.modelname = self.get("modelname")
        self.model_type = ModelType(self.get("modeltype"))


class ImplementationPinAssociationRecord(Record):
    RECORD_ID = 46

    def __init__(self, record):
        super().__init__(record)


class ImplementationPinRecord(Record):
    RECORD_ID = 47

    def __init__(self, record):
        super().__init__(record)
        self.pin_name = self.get("desintf")


class ImplementationParameterListRecord(Record):
    RECORD_ID = 48

    def __init__(self, record):
        super().__init__(record)


RECORD_TYPES = [
    ComponentRecord,
    PinRecord,
    IEEESymbolRecord,
    LabelRecord,
    BezierRecord,
    PolylineRecord,
    PolygonRecord,
    EllipseRecord,
    PiechartRecord,
    RoundedRectangleRecord,
    EllipticalArcRecord,
    ArcRecord,
    LineRecord,
    RectangleRecord,
    SheetSymbolRecord,
    SheetEntryRecord,
    PowerPortRecord,
    PortRecord,
    NoERCRecord,
    NetLabelRecord,
    BusRecord,
    WireRecord,
    TextFrameRecord,
    JunctionRecord,
    ImageRecord,
    SheetRecord,
    SheetNameRecord,
    SheetFilenameRecord,
    DesignatorRecord,
    TemplateFileRecord,
    ParameterRecord,
    WarningSignRecord,
    ImplementationListRecord,
    ImplementationRecord,
    ImplementationPinAssociationRecord,
    ImplementationPinRecord,
    ImplementationParameterListRecord,
]

RECORD_MAP = {rtype.RECORD_ID: rtype for rtype in RECORD_TYPES}


class Color:
    def __init__(self, value):
        if isinstance(value, int):
            self._value = value
        elif isinstance(value, str) and value.startswith("#"):
            self._value = int.from_bytes(bytes.fromhex(value), byteorder="little")
        else:
            raise ValueError(f"Unparsable color: {value}")

    def html(self):
        return f"#{self._value.to_bytes(3, 'little').hex()}"

    def value(self):
        if self._value is not None:
            return self._value
        return 0


class LineStyle(Enum):
    SOLID = 0
    DASHED = 1
    DOTTED = 2
    DASH_DOTTED = 3


class Style(Enum):
    DEFAULT = 0
    ARROW = 1
    BAR = 2
    WAVE = 3
    POWER_GND = 4
    SIGNAL_GND = 5
    EARTH = 6
    GOST_ARROW = 7
    GOST_POWER_GND = 8
    GOST_EARTH = 9
    GOST_BAR = 10


class ModelType(Enum):
    PCBLIB = "PCBLIB"
    SIM = "SIM"
    SI = "SI"
