
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP


def search_products(
    data: dict[str, pd.DataFrame],
    query: str,
    limit: int = 10
) -> list[dict]:

    products = data["products"]
    categories = data["categories"]

    available_products = products[
        (products["status"] == "active") &
        (products["stock_quantity"] > 0)
    ].copy()

    available_products = available_products.merge(
        categories[["category_id", "name"]],
        on="category_id",
        how="left",
        suffixes=("", "_category")
    )

    # Remove palavras que não ajudam na identificação do produto
    stopwords = {
        "quais", "qual", "sao", "estao", "disponiveis",
        "tem", "temos", "de", "da", "do", "com",
        "os", "as", "um", "uma", "para"
    }

    # Separa a consulta em palavras
    query_words = [
        word for word in query.casefold().split()
        if word not in stopwords and len(word) > 2
    ]

    # Combina as informações utilizadas na pesquisa
    search_text = (
        available_products["name"].fillna("") + " " +
        available_products["description"].fillna("") + " " +
        available_products["name_category"].fillna("")
    ).str.casefold()

    # Exige que todas as palavras relevantes sejam encontradas
    mask = pd.Series(True, index=available_products.index)

    for word in query_words:
        mask &= search_text.str.contains(
            word,
            regex=False,
            na=False
        )

    available_products = available_products[mask]

    available_products = available_products.head(limit)

    return available_products[
        [
            "product_id",
            "name",
            "name_category",
            "description",
            "price_brl",
            "stock_quantity"
        ]
    ].rename(
        columns={"name_category": "category"}
    ).to_dict(orient="records")
def get_product_price(
    data: dict[str, pd.DataFrame],
    product_id: int,
    payment_method: str = "credit"
) -> dict:


    if payment_method not in {"pix", "credit", "debit"}:
        raise ValueError("Forma de pagamento inválida.")

    products = data["products"]
    promotions = data["promotions"]

  
    product = products[
        products["product_id"] == product_id
    ]

    if product.empty:
        raise ValueError(f"Produto {product_id} não encontrado.")

    product = product.iloc[0]

   
    original_price = Decimal(str(product["price_brl"]))

   
    active_promotions = promotions[
        (promotions["product_id"] == product_id) &
        (promotions["is_active"] == 1)
    ]

  
    if len(active_promotions) > 1:
        raise ValueError(
            f"Mais de uma promoção ativa para o produto {product_id}."
        )

    promotion_percent = Decimal("0")

    if not active_promotions.empty:
        promotion_percent = Decimal(
            str(active_promotions.iloc[0]["discount_percent"])
        )

   
    if not Decimal("0") <= promotion_percent <= Decimal("100"):
        raise ValueError("Percentual de promoção inválido.")

   
    promotion_discount = (
        original_price * promotion_percent / Decimal("100")
    )

    promotional_price = original_price - promotion_discount

   
    pix_discount = Decimal("0")

    if payment_method == "pix" and promotion_percent == 0:
        pix_discount = original_price * Decimal("0.05")

    final_price = promotional_price - pix_discount

    
    def money(value: Decimal) -> str:
        return str(
            value.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )
        )

    return {
        "product_id": int(product["product_id"]),
        "product_name": product["name"],
        "original_price": money(original_price),
        "promotion_percent": str(promotion_percent),
        "promotion_discount": money(promotion_discount),
        "promotional_price": money(promotional_price),
        "pix_discount": money(pix_discount),
        "payment_method": payment_method,
        "final_price": money(final_price),
        "stock_quantity": int(product["stock_quantity"]),
        "status": product["status"]
    }