from kivy.network.urlrequest import UrlRequest


class CurrencyManager(object):

    def __init__(self):
        self.url = "https://free.currconv.com/"
        self.api_key = 'bfc0324d084dd91c0e6f'

    def get_currencies(self, on_complete, on_failure):
        endpoint = f"api/v7/currencies?apiKey={self.api_key}"
        url = self.url + endpoint

        def receiving_data(request, result):
            data = result['results']
            data = list(data.items())
            data.sort()
            currency_lst = []
            for name, currency in data:
                name = currency['currencyName']
                ids = currency['id']
                symbol = currency.get('currencySymbol', '')
                currency_lst.append({'text': f'{ids} - {name} - {symbol}', 'font_size': 24})
            if on_complete:
                on_complete(currency_lst)

        def data_failing(request, result):
            if on_failure:
                on_failure('Server Error - Try again Later')

        def data_error(request, result):
            if on_failure:
                on_failure('Check your internet connection')

        req = UrlRequest(url, on_success=receiving_data, on_failure=data_failing, on_error=data_error)

    def get_exchange_rate(self, currency_one, currency_two, on_complete, on_failure):
        endpoint = f'api/v7/convert?q={currency_one}_{currency_two}&compact=ultra&apiKey={self.api_key}'
        url = self.url + endpoint

        def receiving_rate(request, result):
            rate = list(result.values())[0]
            if on_complete:
                on_complete(rate)

        def rate_failing(request, result):
            if on_failure:
                on_failure('Server Error')

        def rate_error(request, result):
            if on_failure:
                on_failure('Check your internet connection')

        req = UrlRequest(url, on_success=receiving_rate, on_failure=rate_failing, on_error=rate_error, timeout=1)

    def get_list_currencies(self, on_complete, on_failure):
        endpoint = f"api/v7/currencies?apiKey={self.api_key}"
        url = self.url + endpoint

        def receiving_data(request, result):
            data = result['results']
            data = list(data.items())
            data.sort()
            menu_list = []
            for _, curr in data:
                abbreviation = curr['currencyName']
                ids = curr['id']
                symbol = curr.get('currencySymbol', '')
                menu_list.append((ids, abbreviation, symbol))
            if on_complete:
                on_complete(menu_list)

        def data_failing(request, result):
            if on_failure:
                on_failure('Server Error')

        def data_error(request, result):
            if on_failure:
                on_failure('Check your internet connection')

        req = UrlRequest(url, on_success=receiving_data, on_failure=data_failing, on_error=data_error)
