#!/usr/bin/env python3
"""
Source de données "fichier" pour ChatRH.

Au lieu d'une base PostgreSQL, on extrait et indexe le Code du travail depuis
le fichier DOCX `Code_du_travail_SN` (présent à la racine du projet).
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional
import re
import unicodedata
import zipfile
from xml.etree import ElementTree as ET

from app.config import settings


@dataclass(frozen=True)
class _Store:
    sujets: List[Dict]
    articles: List[Dict]
    sujet_by_id: Dict[int, Dict]
    articles_by_sujet: Dict[int, List[Dict]]
    article_by_id: Dict[int, Dict]
    article_by_num_lower: Dict[str, Dict]


_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

_RE_TITRE = re.compile(r"^\s*Titre\s+(\d+)\s*-\s*(.+?)\s*$", re.IGNORECASE)
# Ex: "Art.L.1.- ..." (le DOCX semble utiliser ce format)
_RE_ART = re.compile(
    r"^\s*Art\.?\s*L\.?\s*(\d+(?:-\d+)?)\s*\.-\s*(.*)\s*$",
    re.IGNORECASE,
)

_RE_QUERY_ART_NUM = re.compile(
    r"(?:(?:\bart(?:icle)?\.?\b)\s*)?(?:\bl\.?\s*)?(\d+(?:-\d+)?)\b",
    re.IGNORECASE,
)

# Ex. "Chapitre 1 - De l'objet des syndicats professionnels"
_RE_CHAPITRE_HEAD = re.compile(
    r"^\s*Chapitre\s+(\d+)\s*(?:-\s*(.+))?\s*$",
    re.IGNORECASE,
)


def _project_root() -> Path:
    # app/ is inside project root
    return Path(__file__).resolve().parents[2]


def _default_docx_path() -> Path:
    return _project_root() / "Code_du_travail_SN"

def _resolve_docx_path(path_str: str) -> Path:
    """
    Résout le chemin vers un fichier .docx.
    - Si `path_str` pointe vers un dossier: prend le premier *.docx trouvé.
    - Si vide: essaie quelques noms par défaut à la racine du projet.
    """
    root = _project_root()

    candidates: List[Path] = []
    if path_str:
        p = Path(path_str)
        if p.is_dir():
            candidates.extend(sorted(p.glob("*.docx")))
        else:
            candidates.append(p)
    else:
        candidates.append(_default_docx_path())
        candidates.append(root / "Code_du_travail_SN.docx")
        candidates.append(root / "Code_sn.docx")

    for c in candidates:
        if c.exists() and c.is_file() and c.suffix.lower() == ".docx":
            return c

    # Dernière chance: si on a un fichier sans extension mais au format docx (zip),
    # on laisse la suite lever une erreur explicite.
    for c in candidates:
        if c.exists() and c.is_file():
            return c

    raise FileNotFoundError(
        "Fichier Code du travail introuvable. "
        "Définissez CODE_TRAVAIL_PATH vers un fichier .docx (ou un dossier contenant un .docx)."
    )


def _extract_docx_paragraphs(docx_path: Path) -> List[str]:
    """
    Extrait le texte du DOCX en conservant les paragraphes.
    Ne dépend d'aucune lib externe (pas de python-docx).
    """
    with zipfile.ZipFile(docx_path, "r") as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)

    paragraphs: List[str] = []
    for p in root.findall(".//w:p", _NS):
        parts = [t.text for t in p.findall(".//w:t", _NS) if t.text]
        if not parts:
            continue
        text = "".join(parts).replace("\xa0", " ").strip()
        if text:
            paragraphs.append(text)
    return paragraphs


def _normalize_text(s: str) -> str:
    """
    Normalisation "recherche":
    - minuscules / casefold
    - suppression des accents (NFKD)
    - correction de mojibake fréquent ("congÃ©" -> "congé")
    - apostrophes typographiques -> apostrophe simple
    - espaces normalisés
    """
    if not s:
        return ""
    # Correction de mojibake courant sur Windows/terminaux: UTF-8 lu comme latin-1/cp1252
    if "Ã" in s or "Â" in s:
        try:
            s = s.encode("latin-1").decode("utf-8")
        except Exception:
            pass
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    s = s.replace("\u00a0", " ")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.casefold()
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _parse_article_num_from_query(q: str) -> Optional[str]:
    """
    Extrait un numéro d'article depuis une requête utilisateur.
    Accepte: "L.148", "L148", "article 148", "Art L 148", "art. l.148", etc.
    Retourne une forme canonique: "l.148" ou "l.148-2".
    """
    if not q:
        return None
    qn = _normalize_text(q)
    # Autoriser aussi "l148" (sans point / espace)
    qn = re.sub(r"\bl(\d)", r"l.\1", qn)
    m = _RE_QUERY_ART_NUM.search(qn)
    if not m:
        return None
    num = m.group(1)
    return f"l.{num}"


def _build_store_from_paragraphs(paragraphs: List[str]) -> _Store:
    sujets: List[Dict] = []
    articles: List[Dict] = []

    # Sujet par défaut si on ne détecte aucun "Titre x - ..."
    current_sujet_id = 1
    current_sujet_title = "Code du travail (Sénégal)"
    sujets.append(
        {
            "id": current_sujet_id,
            "titre_sujet": current_sujet_title,
            "description": "Source: Code du travail sénégalais (DOCX)",
        }
    )
    sujet_title_to_id = {current_sujet_title.lower(): current_sujet_id}

    current_article_num: Optional[str] = None  # ex: "L.1"
    current_article_buf: List[str] = []
    current_article_sujet_id = current_sujet_id
    current_chapitre: Optional[str] = None
    current_chapitre_num: Optional[int] = None

    def flush_article():
        nonlocal current_article_num, current_article_buf, current_article_sujet_id
        if not current_article_num:
            return
        contenu = "\n".join([s for s in current_article_buf if s]).strip()
        if contenu:
            article_id = len(articles) + 1
            article = {
                "article_id": article_id,
                "id_sujet": current_article_sujet_id,
                "num_article": current_article_num,
                "source": "Code_du_travail_SN",
                "chapitre": current_chapitre,
                "chapitre_num": current_chapitre_num,
                "contenu": contenu,
                # champ interne (utilisé pour la recherche tolérante aux accents)
                "contenu_norm": _normalize_text(contenu),
            }
            articles.append(article)
        current_article_num = None
        current_article_buf = []

    for para in paragraphs:
        # Détecter un titre (sujet)
        mt = _RE_TITRE.match(para)
        if mt:
            num = mt.group(1)
            lib = mt.group(2).strip()
            # Éviter de prendre le sommaire (table des matières) comme un sujet
            if lib.count(".") > 20 or "sommaire" in _normalize_text(lib):
                continue
            flush_article()
            current_chapitre = None
            current_chapitre_num = None
            titre = f"Titre {num} - {lib}"
            key = titre.lower()
            if key not in sujet_title_to_id:
                new_id = max(s["id"] for s in sujets) + 1
                sujet = {"id": new_id, "titre_sujet": titre, "description": lib}
                sujets.append(sujet)
                sujet_title_to_id[key] = new_id
            current_sujet_id = sujet_title_to_id[key]
            current_sujet_title = titre
            continue

        mch = _RE_CHAPITRE_HEAD.match(para)
        if mch:
            flush_article()
            cn = int(mch.group(1))
            lib = (mch.group(2) or "").strip()
            current_chapitre_num = cn
            current_chapitre = (
                f"Chapitre {cn}" + (f" - {lib}" if lib else "")
            ).strip()
            continue

        # Détecter un article
        ma = _RE_ART.match(para)
        if ma:
            flush_article()
            num = ma.group(1)
            rest = ma.group(2).strip()
            current_article_num = f"L.{num}"
            current_article_sujet_id = current_sujet_id
            current_article_buf = [rest] if rest else []
            continue

        # Contenu courant (si on est dans un article)
        if current_article_num:
            current_article_buf.append(para)

    flush_article()

    sujet_by_id = {s["id"]: s for s in sujets}
    articles_by_sujet: Dict[int, List[Dict]] = {}
    article_by_id: Dict[int, Dict] = {}
    article_by_num_lower: Dict[str, Dict] = {}

    for a in articles:
        article_by_id[a["article_id"]] = a
        articles_by_sujet.setdefault(a["id_sujet"], []).append(a)
        article_by_num_lower[a["num_article"].lower()] = a

    # Trier les articles par sujet + num (approx)
    for sid, lst in articles_by_sujet.items():
        lst.sort(key=lambda x: x["article_id"])

    return _Store(
        sujets=sujets,
        articles=articles,
        sujet_by_id=sujet_by_id,
        articles_by_sujet=articles_by_sujet,
        article_by_id=article_by_id,
        article_by_num_lower=article_by_num_lower,
    )


@lru_cache(maxsize=1)
def _get_store() -> _Store:
    docx_path_str = getattr(settings, "CODE_TRAVAIL_PATH", "") or ""
    docx_path = _resolve_docx_path(docx_path_str)
    paragraphs = _extract_docx_paragraphs(docx_path)
    return _build_store_from_paragraphs(paragraphs)


# --- API publique (même surface que db_postgres.py) ---

def get_db_connection():
    """Compat: plus de DB en mode fichier."""
    return None


def get_all_sujets() -> List[Dict]:
    return _get_store().sujets


def get_sujet_by_id(sujet_id: int) -> Optional[Dict]:
    return _get_store().sujet_by_id.get(sujet_id)


def get_articles_by_sujet(id_sujet: int) -> List[Dict]:
    return list(_get_store().articles_by_sujet.get(id_sujet, []))


def get_sujet_grouped_by_chapitre(sujet_id: int) -> Optional[Dict[str, Any]]:
    """
    Articles d'un titre (sujet) regroupés par chapitre, pour une API / UI hiérarchique.
    Retourne None si le sujet n'existe pas.
    """
    store = _get_store()
    sujet = store.sujet_by_id.get(sujet_id)
    if not sujet:
        return None
    articles = list(store.articles_by_sujet.get(sujet_id, []))
    sans_chapitre: List[Dict] = []
    buckets: Dict[int, Dict[str, Any]] = {}
    for a in articles:
        cn = a.get("chapitre_num")
        ch = a.get("chapitre")
        if cn is None or not ch:
            sans_chapitre.append(a)
            continue
        if cn not in buckets:
            buckets[cn] = {
                "chapitre_num": cn,
                "chapitre": ch,
                "articles": [],
            }
        buckets[cn]["articles"].append(a)
    chapitres = sorted(buckets.values(), key=lambda x: x["chapitre_num"])
    return {
        "sujet": sujet,
        "chapitres": chapitres,
        "articles_sans_chapitre": sans_chapitre,
    }


def get_article_by_id(article_id: int) -> Optional[Dict]:
    return _get_store().article_by_id.get(article_id)


def search_articles(keyword: str, limit: int = 10) -> List[Dict]:
    """
    Recherche simple (in-memory) par mot-clé dans `contenu`, `chapitre` et `num_article`.
    Supporte aussi les requêtes type "L.148" ou "art l.148".
    """
    if not keyword:
        return []
    store = _get_store()
    q_raw = keyword.strip()
    q_norm = _normalize_text(q_raw)

    # Recherche exacte par numéro d'article si possible
    num = _parse_article_num_from_query(q_raw)
    if num:
        hit = store.article_by_num_lower.get(num.lower())
        if hit:
            return [hit]

    results: List[Dict] = []
    for a in store.articles:
        chap_n = _normalize_text(a.get("chapitre") or "")
        if (
            q_norm in a.get("contenu_norm", "")
            or q_norm in _normalize_text(a["num_article"])
            or (chap_n and q_norm in chap_n)
        ):
            results.append(a)
            if len(results) >= limit:
                break
    return results


def get_article_by_num_article(num_article: str) -> Optional[Dict]:
    """
    Récupère un article par numéro (ex: "L.148", "L148", "148", "art l 148").
    """
    store = _get_store()
    num = _parse_article_num_from_query(num_article)
    if not num:
        # cas: l'utilisateur met juste "148"
        raw = _normalize_text(num_article)
        if re.fullmatch(r"\d+(?:-\d+)?", raw or ""):
            num = f"l.{raw}"
    if not num:
        return None
    return store.article_by_num_lower.get(num.lower())


def get_articles_count() -> int:
    return len(_get_store().articles)


