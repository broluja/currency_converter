from requests import get
from pprint import PrettyPrinter

printer = PrettyPrinter()

URL = "https://free.currconv.com/"
API_KEY = 'bfc0324d084dd91c0e6f'


def get_currencies():
    endpoint = f"api/v7/currencies?apiKey={API_KEY}"
    url = URL + endpoint
    data = get(url).json()['results']

    data = list(data.items())
    data.sort()

    return data


def print_currencies(currencies):
    for name, currency in currencies:
        name = currency['currencyName']
        ids = currency['id']
        symbol = currency.get('currencySymbol', '')
        print(f'{ids} - {name} - {symbol}')
        return currencies


def exchange_rate(currency_one, currency_two):
    endpoint = f'api/v7/convert?q={currency_one}_{currency_two}&compact=ultra&apiKey={API_KEY}'
    url = URL + endpoint
    data = get(url).json()
    if len(data) == 0:
        output = 'Invalid currencies!'
        print(output)

    rate = list(data.values())[0]
    return rate


def buy_foreign_currency(currency_one, currency_two, amount):
    rate = exchange_rate(currency_one, currency_two)
    if rate is None:
        return

    try:
        amount = float(amount)
    except Exception as e:
        print('Invalid Amount')
        print(e.args)
        return

    converted_amount = round(rate * amount, 2)
    print(f'{amount} {currency_one} is equal to {converted_amount}')
    return converted_amount


def main():
    currencies = get_currencies()

    print('Welcome to the currency converter!!')
    print('List - lists the different currencies')
    print('Convert - convert from one currency to another')
    print('Rate - get the exchange rate of two currencies')
    print('------------------------------------------------')

    while True:
        command = input('Enter a command (q to quit): ')
        if command == 'q':
            break
        elif command == 'list':
            print_currencies(currencies)

        elif command == 'convert':
            currency_one = input('Enter a base currency: ').upper()
            amount = input(f'Enter an amount in {currency_one}: ')
            currency_two = input('Enter a currency to convert to: ').upper()
            buy_foreign_currency(currency_one, currency_two, amount)

        elif command == 'rate':
            currency_one = input('Enter a base currency: ').upper()
            currency_two = input('Enter a currency to convert to: ').upper()
            exchange_rate(currency_one, currency_two)

        else:
            print('Unrecognized command!!')
