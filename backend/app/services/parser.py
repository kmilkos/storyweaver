from __future__ import annotations

from pathlib import Path

import fitz


def extract_text_from_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_text_from_pdf(path: Path) -> str:
    doc = fitz.open(str(path))
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return text


def extract_text(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".txt":
        return extract_text_from_txt(path)
    elif ext == ".pdf":
        return extract_text_from_pdf(path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")


def guess_title_from_filename(filename: str) -> str:
    name = Path(filename).stem
    name = name.replace("_", " ").replace("-", " ")
    return name.strip().title()
