#!/usr/bin/env python3
"""Reject PPTX decks with weak scale, wrong aspect ratio or OGP font drift."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
from typing import Optional
import zipfile
import xml.etree.ElementTree as ET

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
EMU_PER_INCH = 914400


def slide_number(name: str) -> int:
    return int(re.search(r"slide(\d+)\.xml$", name).group(1))


def shape_text(shape: ET.Element) -> str:
    return " ".join(
        (node.text or "").strip()
        for node in shape.findall(f".//{{{A}}}t")
        if (node.text or "").strip()
    )


def shape_top(shape: ET.Element) -> Optional[float]:
    off = shape.find(f"./{{{P}}}spPr/{{{A}}}xfrm/{{{A}}}off")
    if off is None or off.get("y") is None:
        return None
    return int(off.get("y")) / EMU_PER_INCH


def shape_sizes(shape: ET.Element) -> list[float]:
    return [int(node.get("sz")) / 100 for node in shape.iter() if node.get("sz")]


def audit(path: Path, ogp: bool) -> list[str]:
    failures: list[str] = []
    with zipfile.ZipFile(path) as package:
        names = package.namelist()
        slides = sorted(
            (name for name in names if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)),
            key=slide_number,
        )
        if not slides:
            return [f"{path.name}: no slides found"]

        presentation = ET.fromstring(package.read("ppt/presentation.xml"))
        slide_size = presentation.find(f"{{{P}}}sldSz")
        if slide_size is not None:
            ratio = int(slide_size.get("cx")) / int(slide_size.get("cy"))
            if abs(ratio - 16 / 9) > 0.01:
                failures.append(f"{path.name}: slide ratio is {ratio:.3f}, not 16:9")

        for position, name in enumerate(slides, start=1):
            root = ET.fromstring(package.read(name))
            title_sizes: list[float] = []
            for shape in root.findall(f".//{{{P}}}sp"):
                text = shape_text(shape)
                sizes = shape_sizes(shape)
                if not text or not sizes:
                    continue
                top = shape_top(shape)
                if position == 1 or (top is not None and top < 2.8):
                    title_sizes.extend(sizes)
                if len(text) >= 35 and max(sizes) < 18:
                    failures.append(
                        f"{path.name} slide {position}: long text falls to {max(sizes):g}pt; expected at least 18pt"
                    )
            title_size = max(title_sizes, default=0)
            title_minimum = 50 if position == 1 else 40
            if title_size < title_minimum:
                failures.append(
                    f"{path.name} slide {position}: title hierarchy peaks at {title_size:g}pt; expected at least {title_minimum}pt"
                )

        if ogp:
            parts = [
                name
                for name in names
                if name.endswith(".xml")
                and (re.fullmatch(r"ppt/slides/slide\d+\.xml", name) or "/theme/" in name)
            ]
            wrong_fonts: set[str] = set()
            for name in parts:
                root = ET.fromstring(package.read(name))
                for script in ("latin", "ea", "cs"):
                    for node in root.findall(f".//{{{A}}}{script}"):
                        typeface = node.get("typeface")
                        if typeface and typeface != "Helvetica Neue":
                            wrong_fonts.add(typeface)
            if wrong_fonts:
                failures.append(
                    f"{path.name}: OGP text or theme fonts include {', '.join(sorted(wrong_fonts))}; expected Helvetica Neue"
                )
            if presentation.find(f"{{{P}}}embeddedFontLst") is not None or any(
                name.startswith("ppt/fonts/") for name in names
            ):
                failures.append(f"{path.name}: embedded font payload remains")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--ogp", action="store_true")
    args = parser.parse_args()
    failures = [failure for path in args.files for failure in audit(path, args.ogp)]
    if failures:
        for failure in failures:
            print("FAIL:", failure)
        return 1
    print("PASS: PPTX quality audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
