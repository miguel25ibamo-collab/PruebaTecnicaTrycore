from flask import Blueprint, jsonify, request

bp = Blueprint("main", __name__)

# --- RUTA DE PRUEBA ---
@bp.get("/")
def home():
    return jsonify(ok=True, message="Flask esta funcionando")


# --- 1) ENDPOINT /calculate-stock ---
@bp.route("/calculate-stock", methods=["POST"])
def calculate_stock():
    """
    BUY suma cantidades, SELL resta cantidades.
    """
    data = request.get_json()

    # Validar que el JSON tenga 'transactions'
    if not data or "transactions" not in data:
        return jsonify(error="El JSON debe contener 'transactions'"), 400

    stock = {}

    for tx in data["transactions"]:
        product = tx.get("productType")
        qty = tx.get("quantity")
        tx_type = tx.get("transactionType")

        # Validaciones básicas
        if not product or not isinstance(qty, int) or tx_type not in ["BUY", "SELL"]:
            return jsonify(error=f"Transacción inválida: {tx}"), 400

        if product not in stock:
            stock[product] = 0

        if tx_type == "BUY":
            stock[product] += qty
        elif tx_type == "SELL":
            stock[product] -= qty

    return jsonify(finalStock=stock), 200

# --- 2) ENDPOINT /product-profit/<product-name> ---
@bp.post("/product-profit/<product_name>")
def product_profit(product_name):
    data = request.get_json(silent=True)

    # Validar que haya JSON y transactions
    if not data or "transactions" not in data:
        return jsonify(error="El JSON debe contener 'transactions'"), 400

    transactions = data.get("transactions", [])
    total_profit = 0
    found = False

    for tx in transactions:
        try:
            product = tx["productType"]
            qty = int(tx["quantity"])
            value = int(tx["unitValue"])
            tx_type = tx["transactionType"]
        except (KeyError, ValueError, TypeError):
            return jsonify(error=f"Transacción inválida: {tx}"), 400

        if product.upper() == product_name.upper() and tx_type == "SELL":
            total_profit += qty * value
            found = True

    if not found:
        return jsonify(error=f"No se encontraron ventas para {product_name}"), 400

    return jsonify(product=product_name.upper(), totalProfit=total_profit), 200