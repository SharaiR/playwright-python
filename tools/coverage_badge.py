from __future__ import annotations
import sys, json
from pathlib import Path
from xml.etree import ElementTree as ET


def pick_color(pct: float) -> str:
    if pct >= 90:
        return "brightgreen"
    if pct >= 80:
        return "green"
    if pct >= 70:
        return "yellowgreen"
    if pct >= 60:
        return "yellow"
    if pct >= 50:
        return "orange"
    return "red"


def main(xml_path: str, out_json: str) -> None:
    root = ET.parse(xml_path).getroot()
    pct = 0.0
    if "line-rate" in root.attrib:
        pct = float(root.attrib["line-rate"]) * 100.0
    else:
        valid = float(root.attrib.get("lines-valid", 0))
        covered = float(root.attrib.get("lines-covered", 0))
        pct = (covered / valid * 100.0) if valid else 0.0
    data = {
        "schemaVersion": 1,
        "label": "coverage",
        "message": f"{pct:.1f}%",
        "color": pick_color(pct),
    }
    Path(out_json).parent.mkdir(parents=True, exist_ok=True)
    Path(out_json).write_text(json.dumps(data), encoding="utf-8")


if __name__ == "__main__":
    xml = sys.argv[1] if len(sys.argv) > 1 else "artifacts/coverage.xml"
    out = sys.argv[2] if len(sys.argv) > 2 else "site/coverage.json"
    main(xml, out)
