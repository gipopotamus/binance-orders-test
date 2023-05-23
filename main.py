from binance.client import Client
import random
import requests

def check_order_price(side, current_price, order_price):
    if side == 'SELL' and order_price < current_price:
        return True
    elif side == 'BUY' and order_price > current_price:
        return True
    return False

# Получение текущей цены с помощью API Binance
def get_current_price(symbol):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        current_price = float(data['price'])
        return current_price
    else:
        raise Exception('Ошибка получения текущей цены')


def create_orders(data, symbol):
    if 'volume' not in data or 'number' not in data or 'amountDif' not in data or 'side' not in data or 'priceMin' not in data or 'priceMax' not in data:
        raise ValueError('Некорректные входные данные')
    if not isinstance(data['volume'], float) or not isinstance(data['number'], int) or not isinstance(data['amountDif'],
                                                                                                      float) \
            or not isinstance(data['side'], str) or not isinstance(data['priceMin'], float) or not isinstance(
        data['priceMax'], float):
        raise ValueError('Некорректные типы данных')
    if data['volume'] <= 0 or data['priceMin'] >= data['priceMax']:
        raise ValueError('Некорректные значения входных данных')
    if data['side'] not in ['SELL', 'BUY']:
        raise ValueError('Некорректное значение стороны торговли')


    volume = data['volume']
    number = data['number']
    amount_dif = data['amountDif']
    side = data['side']
    price_min = data['priceMin']
    price_max = data['priceMax']

    order_price = random.uniform(data['priceMin'], data['priceMax'])
    current_price = get_current_price(symbol)
    if not check_order_price(data['side'], current_price, order_price):
        raise Exception('Неверная цена ордера')

    account_info = client.get_account()
    if 'balances' not in account_info:
        print('Ошибка получения информации о балансе')
        return

    available_balance = 0.0
    if side == 'BUY':
        for balance in account_info['balances']:
            if balance['asset'] == 'USDT':
                available_balance = float(balance['free'])
                break
    elif side == "SELL":
        for balance in account_info['balances']:
            if balance['asset'] == symbol:
                available_balance = float(balance['free']) * current_price
                break

    if available_balance < volume:
        print('Недостаточно средств на счете')
        return

    # Расчет объема и цены каждого ордера
    order_volume = volume / number
    price_range = price_max - price_min

    for i in range(number):
        # Случайный разброс объема в пределах amount_dif
        random_amount = random.uniform(-amount_dif, amount_dif)
        order_volume += random_amount

        # Случайная цена в пределах указанного диапазона
        order_price = random.uniform(price_min, price_max)

        try:
            # Создание ордера
            order = client.create_order(
                symbol= symbol,
                side=side,
                type='LIMIT',
                timeInForce='GTC',
                quantity=order_volume,
                price=order_price
            )

            print(f"Создан ордер: {order}")
        except Exception as e:
            print(f"Ошибка создания ордера: {str(e)}")

# Пример использования


if __name__ == '__main__':
    symbol =  'BTCUSDT'
    api_key = 'YOUR_API_KEY'
    api_secret = 'YOUR_API_SECRET'
    client = Client(api_key, api_secret)
    data = { #тестовые данные
        "volume": 10000.0,
        "number": 5,
        "amountDif": 50.0,
        "side": "SELL",
        "priceMin": 200.0,
        "priceMax": 300.0
    }
    create_orders(data, symbol)