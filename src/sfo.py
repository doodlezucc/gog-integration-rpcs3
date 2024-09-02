from enum import Enum
from io import BufferedReader
from typing import Dict, List, Tuple, Union


class Sfo:
    def __init__(self, mapping: Dict[str, Union[str, int]]):
        self._mapping = mapping

    def __getitem__(self, key):
        return self._mapping[key]

    def _get_string(self, key) -> str:
        return str(self[key])

    def _get_int(self, key) -> int:
        return int(self[key])

    @property
    def title(self):
        return self._get_string("TITLE")

    @property
    def license(self):
        return self._get_string("LICENSE")

    @property
    def language(self):
        return self._get_string("LANG")


class SfoDecoder:
    DEFAULT_BYTE_ORDER = "little"

    def _seek(self, position: int):
        self.position = position
        return self._reader.seek(position)

    def _read(self, size: int):
        self.position += size
        return self._reader.read(size)

    def _read_integer(self, size: int, signed: bool):
        return int.from_bytes(
            self._read(size),
            byteorder=SfoDecoder.DEFAULT_BYTE_ORDER,
            signed=signed,
        )

    def _read_uint16(self):
        return self._read_integer(2, False)

    def _read_uint32(self):
        return self._read_integer(4, False)

    def _read_int16(self):
        return self._read_integer(2, True)

    def _read_int32(self):
        return self._read_integer(4, True)

    def _read_string_null_terminated(self):
        NULL = 0x00

        utf8_bytes = bytearray()

        read_bytes = self._read(1)
        while read_bytes[0] != NULL:
            utf8_bytes.append(read_bytes[0])

        return str(utf8_bytes, encoding="utf-8")

    def _read_string(self, length: int):
        return str(self._read(length), encoding="utf-8")

    def read_header(self):
        magic = self._read_uint32()
        version = self._read_uint32()
        self.key_table_start = self._read_uint32()
        self.data_table_start = self._read_uint32()
        self.tables_entries = self._read_uint32()

    def read_index_table(self) -> List["SfoEntry"]:
        def read_entry():
            key_offset = self._read_uint16()
            data_fmt = self._read_uint16()
            data_len = self._read_uint32()
            data_max_len = self._read_uint32()
            data_offset = self._read_uint32()

            return SfoEntry(key_offset, data_fmt, data_len, data_max_len, data_offset)

        entries = []
        while self.position < self.key_table_start:
            entries.append(read_entry())

        return entries

    def _extract_key(self, position: int) -> str:
        self._seek(position)
        return self._read_string_null_terminated()

    def _extract_data(self, position: int, length: int, format: int) -> Union[str, int]:
        if length == 0:
            # Reserved entry
            return -1

        self._seek(position)

        if format == SfoEntryFormats.UTF8_SPECIAL:
            return self._read_string(length)
        elif format == SfoEntryFormats.UTF8:
            return self._read_string_null_terminated()
        elif format == SfoEntryFormats.UNSIGNED_INT:
            return self._read_integer(length, False)

        raise KeyError("Unknown data format " + hex(format))

    def _extract_entry_pair(self, entry: "SfoEntry") -> Tuple[str, Union[str, int]]:
        key = self._extract_key(entry.key_offset)
        data = self._extract_data(entry.data_offset, entry.data_len, entry.data_fmt)

        return (key, data)

    # Based on the internal structure described at https://www.psdevwiki.com/ps3/PARAM.SFO
    def decode(self, reader: BufferedReader):
        self._reader = reader
        self.position = 0

        self.read_header()
        entries = self.read_index_table()

        return dict(self._extract_entry_pair(entry) for entry in entries)


class SfoEntryFormats(Enum):
    UTF8_SPECIAL = 0x0400
    UTF8 = 0x0402
    UNSIGNED_INT = 0x0404


class SfoEntry:
    def __init__(
        self,
        key_offset: int,
        data_fmt: int,
        data_len: int,
        data_max_len: int,
        data_offset: int,
    ):
        self.key_offset = key_offset
        self.data_fmt = data_fmt
        self.data_len = data_len
        self.data_max_len = data_max_len
        self.data_offset = data_offset


def decode_sfo_file(path: str):
    decoder = SfoDecoder()

    # Open in binary reading mode
    with open(path, mode="rb") as file:
        return decoder.decode(file)
