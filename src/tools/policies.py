
from pathlib import Path
import re
import unicodedata
import textwrap

from pypdf import PdfReader


BASE_DIR = Path(__file__).resolve().parents[2]
POLICY_FILE = BASE_DIR / "data" / "políticas_da_loja.pdf"


def load_policies() -> list[str]:
    if not POLICY_FILE.exists():
        raise FileNotFoundError(
            f"Arquivo de políticas não encontrado: {POLICY_FILE}"
        )

    reader = PdfReader(POLICY_FILE)
    chunks = []

    for page in reader.pages:
        text = page.extract_text() or ""

        if not text.strip():
            continue

        # Normaliza os espaços e as quebras de linha extraídas do PDF
        text = re.sub(r"\s+", " ", text).strip()

        # Identifica as seções numeradas do documento
        sections = re.split(
            r"(?=\b\d+(?:\.\d+)*\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ])",
            text
        )

        for section in sections:
            section = section.strip()

            if not section:
                continue

            # Divide somente se a seção ultrapassar o limite
            if len(section) > 1800:
                parts = textwrap.wrap(
                    section,
                    width=1800,
                    break_long_words=False,
                    break_on_hyphens=False
                )
                chunks.extend(parts)
            else:
                chunks.append(section)

    if not chunks:
        raise ValueError("Não foi possível extrair texto do PDF.")

    return chunks


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.casefold())

    return "".join(
        char for char in text
        if not unicodedata.combining(char)
    )


def search_policies(query: str, limit: int = 8) -> list[dict]:
    if not query.strip():
        return []

    paragraphs = load_policies()

    stopwords = {
        "a", "as", "o", "os", "um", "uma", "de", "da",
        "do", "das", "dos", "em", "no", "na", "para",
        "por", "com", "e", "ou", "que", "qual", "quais",
        "como", "quando", "me", "minha", "meu", "sobre",
        "loja", "sao", "aceita"
    }

    query_words = {
        word
        for word in normalize_text(query).split()
        if word not in stopwords and len(word) > 2
    }

    results = []

    for paragraph in paragraphs:
        normalized_paragraph = normalize_text(paragraph)
        paragraph_words = set(normalized_paragraph.split())

        matching_words = query_words.intersection(paragraph_words)

        if matching_words:
            score = len(matching_words)

            if query_words.issubset(paragraph_words):
                score += 3

            results.append({
                "text": paragraph,
                "relevance": score
            })

    results.sort(
        key=lambda item: item["relevance"],
        reverse=True
    )

    return results[:limit]
