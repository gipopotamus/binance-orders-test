from binance.client import Client
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
client = Client(config['Binance']['API_KEY'], config['Binance']['API_SECRET'])
Symbol = config['Binance']['SYMBOL']