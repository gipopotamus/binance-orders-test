from flask import Flask, request, jsonify
from order_handler import create_orders

app = Flask(__name__)


@app.route('/create_orders', methods=['POST'])
def handle_create_orders():
    data = request.get_json()
    response = create_orders(data)
    return jsonify(response)


if __name__ == '__main__':
    app.run()
