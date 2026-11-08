from __future__ import annotations

import json
import hashlib
from pathlib import Path

from docx import Document
from openpyxl import load_workbook
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "extracted"
OUT.mkdir(parents=True, exist_ok=True)


def safe_name(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    stem = "__".join(rel.split("/")).replace(" ", "_")
    if len(stem) > 120:
        digest = hashlib.sha1(rel.encode("utf-8")).hexdigest()[:12]
        stem = f"{stem[:100]}__{digest}"
    return stem


manifest: list[dict[str, object]] = []

for path in sorted(ROOT.rglob("*.pdf")):
    reader = PdfReader(str(path))
    chunks = []
    for page_no, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ""
        chunks.append(f"\n===== PAGE {page_no} =====\n{text}")
    output = OUT / f"{safe_name(path)}.txt"
    output.write_text("".join(chunks), encoding="utf-8")
    manifest.append({
        "type": "pdf",
        "path": str(path.relative_to(ROOT)),
        "pages": len(reader.pages),
        "characters": sum(len(c) for c in chunks),
        "extract": str(output.relative_to(ROOT)),
    })

for path in sorted(ROOT.rglob("*.docx")):
    doc = Document(str(path))
    chunks = [p.text for p in doc.paragraphs if p.text.strip()]
    for table_no, table in enumerate(doc.tables, 1):
        chunks.append(f"\n===== TABLE {table_no} =====")
        for row in table.rows:
            chunks.append("\t".join(cell.text.replace("\n", " | ") for cell in row.cells))
    output = OUT / f"{safe_name(path)}.txt"
    output.write_text("\n".join(chunks), encoding="utf-8")
    manifest.append({
        "type": "docx",
        "path": str(path.relative_to(ROOT)),
        "paragraphs": len(doc.paragraphs),
        "tables": len(doc.tables),
        "characters": sum(len(c) for c in chunks),
        "extract": str(output.relative_to(ROOT)),
    })

for path in sorted(ROOT.rglob("*.xlsx")):
    wb = load_workbook(path, read_only=True, data_only=False)
    chunks = []
    sheets = []
    for ws in wb.worksheets:
        sheets.append({"title": ws.title, "max_row": ws.max_row, "max_column": ws.max_column})
        chunks.append(f"\n===== SHEET {ws.title} =====")
        for row in ws.iter_rows():
            values = ["" if cell.value is None else str(cell.value) for cell in row]
            if any(values):
                chunks.append("\t".join(values))
    output = OUT / f"{safe_name(path)}.txt"
    output.write_text("\n".join(chunks), encoding="utf-8")
    manifest.append({
        "type": "xlsx",
        "path": str(path.relative_to(ROOT)),
        "sheets": sheets,
        "characters": sum(len(c) for c in chunks),
        "extract": str(output.relative_to(ROOT)),
    })

for path in sorted(ROOT.rglob("*.md")):
    text = path.read_text(encoding="utf-8", errors="replace")
    manifest.append({
        "type": "markdown",
        "path": str(path.relative_to(ROOT)),
        "lines": text.count("\n") + 1,
        "characters": len(text),
    })

for path in sorted(ROOT.rglob("*.jpg")):
    with Image.open(path) as image:
        manifest.append({
            "type": "image",
            "path": str(path.relative_to(ROOT)),
            "width": image.width,
            "height": image.height,
            "mode": image.mode,
        })

(OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(manifest, ensure_ascii=False, indent=2))
