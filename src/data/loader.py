
from pathlib import Path

import pandas as pd



BASE_DIR = Path(__file__).resolve().parents[2]

# Diretório que contém os arquivos CSV
DATA_DIR = BASE_DIR / "data"



CSV_FILES = {
    "categories": "desafio_tecnico_ai_eng - categories.csv",
    "customers": "desafio_tecnico_ai_eng - customers.csv",
    "orders": "desafio_tecnico_ai_eng - orders.csv",
    "order_items": "desafio_tecnico_ai_eng - order_items.csv",
    "products": "desafio_tecnico_ai_eng - products.csv",
    "promotions": "desafio_tecnico_ai_eng - promotions.csv",
}


def load_data() -> dict[str, pd.DataFrame]:
    """Carrega todos os arquivos CSV e retorna seus DataFrames."""

    data = {}

    for table_name, file_name in CSV_FILES.items():
        file_path = DATA_DIR / file_name

        if not file_path.exists():
            raise FileNotFoundError(
                f"Arquivo não encontrado: {file_path}"
            )

        data[table_name] = pd.read_csv(
            file_path,
            encoding="utf-8-sig"
        )

    return data
