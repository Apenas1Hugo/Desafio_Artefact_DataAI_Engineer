
import pandas as pd


def get_customer_orders(
    data: dict[str, pd.DataFrame],
    customer_id: int
) -> dict:

    customers = data["customers"]
    orders = data["orders"]
    order_items = data["order_items"]
    products = data["products"]

   
    customer = customers[
        customers["customer_id"] == customer_id
    ]

    if customer.empty:
        raise ValueError(f"Cliente {customer_id} não encontrado.")

    customer = customer.iloc[0]

   
    customer_orders = orders[
        orders["customer_id"] == customer_id
    ].copy()

    if customer_orders.empty:
        return {
            "customer_id": int(customer_id),
            "customer_name": customer["name"],
            "orders": []
        }

   
    result_orders = []

    for _, order in customer_orders.iterrows():

        items = order_items[
            order_items["order_id"] == order["order_id"]
        ]

     
        items = items.merge(
            products[["product_id", "name"]],
            on="product_id",
            how="left"
        )

        order_products = []

        for _, item in items.iterrows():
            order_products.append({
                "product_id": int(item["product_id"]),
                "product_name": item["name"],
                "quantity": int(item["quantity"])
            })

      
        result_orders.append({
            "order_id": int(order["order_id"]),
            "order_date": str(order["order_date"]),
            "status": order["status"],
            "total_brl": str(order["total_brl"]),
            "payment_method": order["payment_method"],
            "tracking_code": (
                None if pd.isna(order["tracking_code"])
                else order["tracking_code"]
            ),
            "estimated_delivery": (
                None if pd.isna(order["estimated_delivery"])
                else str(order["estimated_delivery"])
            ),
            "items": order_products
        })

   
    return {
        "customer_id": int(customer_id),
        "customer_name": customer["name"],
        "orders": result_orders
    }
