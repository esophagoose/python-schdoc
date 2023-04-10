import records as types
import olefile
import struct
import zlib
import logging

logging.basicConfig(level=logging.INFO)

EXPECTED_DIRECTORIES = {'Storage', 'Additional', 'FileHeader'}

class Schematic:
    def __init__(self, path: str):
        self.path = path
        self.records = []
        self.files = {}
        self.name = path.split("/")[-1].upper()

    def __str__(self) -> str:
        return f"Schematic<{self.name}>"

    def __repr__(self) -> str:
        return f"Schematic<{self.name}>"

    def check_header(self, header: str) -> bool:
        return "Protel for Windows - Schematic Capture Binary File Version 5.0" in header

    def read(self):
        unparsed_records = []
        with open(self.path, "rb") as datastream:
            ole = olefile.OleFileIO(datastream)
            self.raw_content = ole.openstream("FileHeader").read()
            self.raw_storage = ole.openstream("Storage").read()
            self.raw_additional = ole.openstream("Additional").read()
            unparsed_records = self.read_records(self.raw_content)
            unparsed_records += self.read_records(self.raw_additional)
            self.files = self.read_storage(self.raw_storage)

            directories = set(["".join(dir) for dir in ole.listdir()])
            if directories - EXPECTED_DIRECTORIES:
                diff = directories - EXPECTED_DIRECTORIES
                logging.warn(f"Extra OLE file streams - didn't expect: {diff}")
            logging.info(f"Finished reading in {self.name}")
    
        for ur in unparsed_records:
            self.records.append(self.parse_record(ur))
        # Find all parent / child relationships
        sheets = [r for r in self.records if isinstance(r, types.SheetRecord)]
        if len(sheets) > 1:
            logging.warn("Multiple sheets found!")
        self.sheet = sheets[0]
        return self
    
    def read_records(self, data):
        blocks = []
        streamer = DataStreamer(data)
        while not streamer.eof():
            payload_size = streamer.read_int(2)
            assert streamer.read_int(1) == 0, "Bad pad in header"
            assert streamer.read_int(1) == 0, "Bad type in header"
            payload = streamer.read(payload_size)
            assert payload[-1] == 0, "Invalid ending byte"
            blocks.append(payload[:-1].decode("latin1"))
        if self.check_header(blocks[0]):
            return blocks[1:]
        return blocks


    def read_storage(self, data):
        streamer = DataStreamer(data)
        payload_size = streamer.read_int(2)
        assert streamer.read_int(1) == 0, "Bad pad in header"
        assert streamer.read_int(1) == 0, "Bad type in header"
        header = streamer.read(payload_size)
        if b"|HEADER=Icon storage" not in header or header[-1] != 0:
            raise ValueError(f"Invalid header: {header}")

        # Read in data
        images = {}
        while not streamer.eof():
            streamer.read_int(2)  # payload size; not used
            if streamer.read_int(1) == 0:
                logging.warning("Bad padding found!")
            if streamer.read_int(1) == 1:
                logging.warning("Bad type found!")
            if streamer.read_int(1) == 0xD0:
                logging.warning("Bad magic value found!")
            filename_length = streamer.read_int(1)
            filename = streamer.read(filename_length)
            compressed_size = streamer.read_int(4)
            image = zlib.decompress(streamer.read(compressed_size))
            images[filename] = image
        return images

    def parse_record(self, data):
        record_id = None
        parameters = {}
        for field in data.split("|"):
            if field:
                (name, value) = field.split("=", 1)
                if name == "RECORD":
                    record_id = int(value)
                parameters[name] = value
        if not record_id:
            logging.error(data)
        return types.RECORD_MAP[record_id](parameters)


class DataStreamer:
    def __init__(self, data) -> None:
        self.data = data
        self.pos = 0

    def read(self, length) -> bytes:
        self.pos += length
        return self.data[self.pos - length:self.pos]

    def read_int(self, length) -> int:
        return int.from_bytes(self.read(length), "little")
    
    def eof(self) -> bool:
        return self.pos + 1 >= len(self.data)



