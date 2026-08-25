#!/usr/bin/env python3
"""Set a PPTX theme and explicit slide text to one installed typeface."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import tempfile
import zipfile
import xml.etree.ElementTree as ET

P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
FONT_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/font"

ET.register_namespace("p", P)
ET.register_namespace("a", A)


def parse(data: bytes) -> ET.Element:
    return ET.fromstring(data)


def serialise(root: ET.Element) -> bytes:
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def patch_content_types(data: bytes) -> bytes:
    ET.register_namespace("", CT)
    root = parse(data)
    for node in list(root):
        if node.tag == f"{{{CT}}}Default" and node.get("Extension") in {"fntdata", "odttf"}:
            root.remove(node)
    return serialise(root)


def patch_relationships(data: bytes) -> bytes:
    ET.register_namespace("", REL)
    root = parse(data)
    for node in list(root):
        if node.get("Type") == FONT_REL:
            root.remove(node)
    return serialise(root)


def patch_presentation(data: bytes) -> bytes:
    root = parse(data)
    embedded = root.find(f"{{{P}}}embeddedFontLst")
    if embedded is not None:
        root.remove(embedded)
    return serialise(root)


def patch_theme(data: bytes, font: str) -> bytes:
    root = parse(data)
    for family in ("majorFont", "minorFont"):
        for script in ("latin", "ea", "cs"):
            for node in root.findall(f".//{{{A}}}{family}/{{{A}}}{script}"):
                node.set("typeface", font)
    return serialise(root)


def patch_text(data: bytes, font: str) -> bytes:
    root = parse(data)
    text_property_tags = {f"{{{A}}}rPr", f"{{{A}}}defRPr", f"{{{A}}}endParaRPr"}
    for props in (node for node in root.iter() if node.tag in text_property_tags):
        for script in ("latin", "ea", "cs"):
            node = props.find(f"{{{A}}}{script}")
            if node is None:
                node = ET.SubElement(props, f"{{{A}}}{script}")
            node.set("typeface", font)
    return serialise(root)


def set_font(pptx: Path, font: str) -> None:
    with zipfile.ZipFile(pptx, "r") as source:
        names = source.namelist()
        required = {"[Content_Types].xml", "ppt/presentation.xml", "ppt/_rels/presentation.xml.rels"}
        absent = required.difference(names)
        if absent:
            raise ValueError("Not a supported PPTX; missing: " + ", ".join(sorted(absent)))

        fd, tmp_name = tempfile.mkstemp(prefix=pptx.stem + "-", suffix=".pptx", dir=pptx.parent)
        os.close(fd)
        tmp = Path(tmp_name)
        try:
            with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as target:
                for item in source.infolist():
                    if item.filename.startswith("ppt/fonts/"):
                        continue
                    data = source.read(item.filename)
                    if item.filename == "[Content_Types].xml":
                        data = patch_content_types(data)
                    elif item.filename == "ppt/presentation.xml":
                        data = patch_presentation(data)
                    elif item.filename == "ppt/_rels/presentation.xml.rels":
                        data = patch_relationships(data)
                    elif item.filename.startswith("ppt/") and "/theme/" in item.filename and item.filename.endswith(".xml"):
                        data = patch_theme(data, font)
                    elif item.filename.startswith("ppt/slides/slide") and item.filename.endswith(".xml"):
                        data = patch_text(data, font)
                    target.writestr(item, data)
            os.replace(tmp, pptx)
        except Exception:
            tmp.unlink(missing_ok=True)
            raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--font", default="Helvetica Neue")
    args = parser.parse_args()
    set_font(args.pptx.resolve(), args.font)


if __name__ == "__main__":
    main()
