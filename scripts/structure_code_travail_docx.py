#!/usr/bin/env python3
"""
Nettoie un export DOCX du Code du travail pour l'indexation par app/db/db_code_travail_docx.py.

Supprime en-têtes / pieds répétitifs, la ligne de sommaire « pointillée », fusionne les
titres coupés sur deux paragraphes, puis écrit un nouveau .docx.

Dépendance : pip install python-docx
"""

from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from docx import Document

_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

_RE_TITRE_LINE = re.compile(r"^\s*Titre\s+\d+\s*-\s*.+$", re.IGNORECASE)
_RE_ART = re.compile(r"^\s*Art\.?\s*L\.", re.IGNORECASE)
_RE_TITRE_NUM = re.compile(r"^\s*Titre\s+\d+", re.IGNORECASE)
_RE_CHAPITRE = re.compile(r"^\s*Chapitre\s+", re.IGNORECASE)


def extract_paragraphs(docx_path: Path) -> list[str]:
    with zipfile.ZipFile(docx_path, "r") as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)
    out: list[str] = []
    for p in root.findall(".//w:p", _NS):
        parts = [t.text for t in p.findall(".//w:t", _NS) if t.text]
        if not parts:
            continue
        text = "".join(parts).replace("\xa0", " ").strip()
        if text:
            out.append(text)
    return out


def is_boilerplate(s: str) -> bool:
    t = s.strip()
    if re.match(r"^www\.", t, re.IGNORECASE):
        return True
    if re.match(r"^Code du travail\s+\d+\s*/\s*\d+", t, re.IGNORECASE):
        return True
    if t.casefold() in ("sénégal", "senegal"):
        return True
    return False


def is_toc_compressed_line(s: str) -> bool:
    """Ligne type sommaire avec de nombreux points de suite."""
    if re.search(r"Titre\s+\d+\s*-", s) is None:
        return False
    return s.count(".") > 15


def merge_split_titles(paras: list[str]) -> list[str]:
    """Fusionne « Titre N - … » et la ligne suivante si c'est la suite du libellé."""
    out: list[str] = []
    i = 0
    while i < len(paras):
        t = paras[i]
        if (
            _RE_TITRE_LINE.match(t)
            and i + 1 < len(paras)
        ):
            nxt = paras[i + 1]
            if (
                not _RE_ART.match(nxt)
                and not _RE_TITRE_NUM.match(nxt)
                and not _RE_CHAPITRE.match(nxt)
                and not nxt.strip().startswith("!")
                and len(nxt) < 160
            ):
                out.append(re.sub(r"\s+", " ", f"{t.rstrip()} {nxt.strip()}"))
                i += 2
                continue
        out.append(t)
        i += 1
    return out


def structure_paragraphs(raw: list[str]) -> list[str]:
    cleaned = [p for p in raw if not is_boilerplate(p) and not is_toc_compressed_line(p)]
    return merge_split_titles(cleaned)


def write_docx(paragraphs: list[str], out_path: Path) -> None:
    doc = Document()
    for line in paragraphs:
        doc.add_paragraph(line)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_path))


def main() -> None:
    parser = argparse.ArgumentParser(description="Structure un DOCX Code du travail pour ChatRH.")
    parser.add_argument(
        "input",
        type=Path,
        nargs="?",
        default=Path("Code_sn.docx"),
        help="Fichier source (.docx)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("Code_sn_structure.docx"),
        help="Fichier de sortie",
    )
    args = parser.parse_args()
    if not args.input.is_file():
        raise SystemExit(f"Fichier introuvable : {args.input}")
    paras = structure_paragraphs(extract_paragraphs(args.input))
    write_docx(paras, args.output)
    print(f"Écrit {len(paras)} paragraphes dans {args.output}")


if __name__ == "__main__":
    main()
