
from pathlib import Path
import re
import unicodedata

from pypdf import PdfReader


BASE_DIR = Path(__file__).resolve().parents[2]
POLICY_FILE = BASE_DIR / "data" / "políticas_da_loja.pdf"


def load_policies() -> list[str]:
    if not POLICY_FILE.exists():
        raise FileNotFoundError(
            f"Arquivo de políticas não encontrado: {POLICY_FILE}"
        )

    reader = PdfReader(POLICY_FILE)

    text = "\n".join(
        page.extract_text() or ""
        for page in reader.pages
    )

    if not text.strip():
        raise ValueError("Não foi possível extrair texto do PDF.")

    
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s*\n\s*", " ", text)

    
    chunks = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    return [
        chunk.strip()
        for chunk in chunks
        if len(chunk.strip()) > 40
    ]


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.casefold())

    return "".join(
        char for char in text
        if not unicodedata.combining(char)
    )


def search_policies(query: str, limit: int = 3) -> list[dict]:

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

          
            for word in query_words:
                if word in paragraph_words:
                    score += 1

            results.append({
                "text": paragraph,
                "relevance": score
            })

   
    results.sort(
        key=lambda item: item["relevance"],
        reverse=True
    )

    return results[:limit]
