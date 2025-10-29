import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

def get_currency_list():
    url = "https://api.frankfurter.app/currencies"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}

@app.route('/')
def index():
    currencies = get_currency_list()
    return render_template("index.html", currencies=currencies)

@app.route('/convert', methods=['POST'])
def convert_currency():
    data = request.get_json()
    amount = float(data.get("amount", 0))
    from_currency = data.get("from")
    to_currency = data.get("to")
    if not amount or not from_currency or not to_currency:
        return jsonify({"error": "ข้อมูลไม่ครบ"}), 400

    try:
        url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        result = data["rates"][to_currency]
        rate = round(result / amount, 4)
        return jsonify({"amount": amount, "from": from_currency, "to": to_currency, "result": result, "rate": rate})
    except:
        return jsonify({"error": "เกิดข้อผิดพลาดในการแปลงเงิน"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

