from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

def get_currency_list():
    url = "https://api.frankfurter.app/currencies"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {}

@app.route('/')
def index():
    currencies = get_currency_list()
    return render_template('index.html', currencies=currencies)

@app.route('/convert', methods=['POST'])
def convert_currency():
    data = request.get_json()
    from_currency = data.get('from')
    to_currency = data.get('to')
    amount = float(data.get('amount', 0))

    url = f"https://api.frankfurter.app/latest?from={from_currency}&to={to_currency}"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "API request failed"}), 500

    result = response.json()
    rate = result["rates"].get(to_currency)
    if not rate:
        return jsonify({"error": "Invalid currency pair"}), 400

    converted = amount * rate

    return jsonify({
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "result": round(converted, 2),
        "rate": round(rate, 4)
    })

if __name__ == '__main__':
    app.run(debug=True)
