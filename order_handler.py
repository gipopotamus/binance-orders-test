import random
from binance_client import client
from config import SYMBOL


def get_current_price():
    try:
        ticker = client.get_ticker(symbol=SYMBOL)
        current_price = float(ticker['lastPrice'])
        return current_price
    except Exception as e:
        return {'error': str(e)}


def create_order(order_data, current_price):
    volume = order_data['volume']
    number = order_data['number']
    amount_dif = order_data['amountDif']
    side = order_data['side']
    price_min = order_data['priceMin']
    price_max = order_data['priceMax']

    if not isinstance(volume, float) or not isinstance(number, int) or not isinstance(amount_dif, float) \
            or not isinstance(side, str) or not isinstance(price_min, float) or not isinstance(price_max, float):
        raise ValueError('Некорректные типы данных в данных ордера')

    if volume <= 0 or price_min >= price_max:
        raise ValueError('Некорректные значения в данных ордера')

    if side not in ['SELL', 'BUY']:
        raise ValueError('Некорректное значение стороны торговли')

    if side == 'SELL' and current_price < price_min:
        raise Exception('Неверная цена ордера')
    elif side == 'BUY' and current_price > price_max:
        raise Exception('Неверная цена ордера')

    account_info = client.get_account()
    available_balance = next((float(balance['free']) for balance in account_info['balances']
                              if (balance['asset'] == 'USDT' and side == 'BUY')
                              or (balance['asset'] == SYMBOL and side == 'SELL')), 0.0)
    if available_balance < volume:
        raise Exception('Недостаточно средств')

    order_volume = volume / number
    for i in range(number):
        # Случайный разброс объема в пределах amount_dif
        random_amount = random.uniform(-amount_dif, amount_dif)
        order_volume += random_amount

        # Случайная цена в пределах указанного диапазона
        order_price = random.uniform(price_min, price_max)

        try:
            # Создание ордера
            order = client.create_order(
                symbol=SYMBOL,
                side=side,
                type='LIMIT',
                timeInForce='GTC',
                quantity=order_volume,
                price=order_price
            )

            print(f"Создан ордер: {order}")
        except Exception as e:
            raise f"Ошибка создания ордера: {str(e)}"


def create_orders(data):
    try:
        symbol = SYMBOL
        orders_data = data.get('orders')

        if not symbol or not orders_data:
            raise ValueError('Некорректные входные данные')

        current_price = get_current_price()

        for order_data in orders_data:
            create_order(order_data, current_price)

        return {'message': 'Ордеры успешно созданы'}
    except Exception as e:
        return {'error': str(e)}
