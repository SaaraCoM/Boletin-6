from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET


MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
DOC_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"


@dataclass(slots=True)
class XlsxSheet:
    name: str
    rows: list[list[str]]


class SimpleXlsxReader:
    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)

    def read_sheets(self) -> list[XlsxSheet]:
        with ZipFile(self.file_path) as archive:
            shared_strings = self._read_shared_strings(archive)
            workbook = ET.fromstring(archive.read("xl/workbook.xml"))
            rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
            relmap = {}
            for relation in rels:
                relation_id = relation.attrib.get("Id")
                target = relation.attrib.get("Target", "")
                relmap[relation_id] = target
            sheets = []
            sheets_node = workbook.find(f"{{{MAIN_NS}}}sheets")
            if sheets_node is None:
                return sheets
            for sheet in sheets_node:
                name = sheet.attrib.get("name", "")
                relation_id = sheet.attrib.get(f"{{{DOC_REL_NS}}}id", "")
                target = relmap.get(relation_id, "")
                if not target:
                    continue
                xml_path = f"xl/{target}"
                rows = self._read_rows(archive.read(xml_path), shared_strings)
                sheets.append(XlsxSheet(name=name, rows=rows))
            return sheets

    def _read_shared_strings(self, archive: ZipFile) -> list[str]:
        try:
            xml_bytes = archive.read("xl/sharedStrings.xml")
        except KeyError:
            return []
        root = ET.fromstring(xml_bytes)
        values: list[str] = []
        for item in root.findall(f"{{{MAIN_NS}}}si"):
            parts: list[str] = []
            for text_node in item.iter(f"{{{MAIN_NS}}}t"):
                parts.append(text_node.text or "")
            values.append("".join(parts))
        return values

    def _read_rows(self, xml_bytes: bytes, shared_strings: list[str]) -> list[list[str]]:
        worksheet = ET.fromstring(xml_bytes)
        sheet_data = worksheet.find(f"{{{MAIN_NS}}}sheetData")
        if sheet_data is None:
            return []
        rows: list[list[str]] = []
        for row in sheet_data:
            cells = {}
            max_index = -1
            for cell in row.findall(f"{{{MAIN_NS}}}c"):
                reference = cell.attrib.get("r", "A1")
                column_name = self._extract_column_name(reference)
                column_index = self._column_name_to_index(column_name)
                cell_type = cell.attrib.get("t")
                value_node = cell.find(f"{{{MAIN_NS}}}v")
                if value_node is None:
                    value = ""
                else:
                    value = value_node.text or ""
                if cell_type == "s" and value:
                    value = shared_strings[int(value)]
                cells[column_index] = value
                if column_index > max_index:
                    max_index = column_index
            normalized = []
            for index in range(max_index + 1):
                normalized.append(cells.get(index, ""))
            rows.append(normalized)
        return rows

    def _extract_column_name(self, reference: str) -> str:
        chars = []
        for char in reference:
            if char.isalpha():
                chars.append(char)
            else:
                break
        return "".join(chars)

    def _column_name_to_index(self, name: str) -> int:
        result = 0
        for char in name:
            result = result * 26 + (ord(char.upper()) - 64)
        return result - 1
