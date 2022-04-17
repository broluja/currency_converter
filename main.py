from kivy.config import Config

Config.set("graphics", "width", "630")
Config.set("graphics", "height", "950")

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.properties import NumericProperty, ObjectProperty, ListProperty, StringProperty
from kivy.lang import Builder

from currency_manager import CurrencyManager


class RV(RecycleView):
    error = StringProperty()

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []
        CurrencyManager().get_currencies(self.on_server_data, self.on_server_failure)

    def on_server_data(self, data):
        self.data = data

    def on_server_failure(self, error):
        self.data.append({'text': error})


class MyLayout(BoxLayout):
    state = NumericProperty(0)
    recycleView = ObjectProperty(None)
    menu = ObjectProperty()
    menu_list = ListProperty()
    dropdown_list = ListProperty()
    rate = NumericProperty()
    error = StringProperty('Error')

    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        CurrencyManager().get_list_currencies(self.on_server_data, self.on_server_failure)
        self.get_exchange_rate('EUR', 'RSD')

    def on_server_data(self, data):
        self.menu_list = data

    def on_server_failure(self, error):
        self.error = error
        self.ids.result.theme_text_color = 'Error'
        self.ids.result.text = self.error

    def open_menu_one(self):
        for ids, abbreviation, symbol in self.menu_list:
            self.dropdown_list.append(
                {'viewclass': 'OneLineListItem',
                 'text': f'{ids} - {abbreviation} - {symbol}',
                 'on_press': lambda x=f'{ids} - {symbol}': self.option_callback(x)}
            )
        self.menu = MDDropdownMenu(width_mult=4)
        self.menu.caller = self.ids.drop_item_one
        self.menu.items = self.dropdown_list
        self.menu.open()

    def open_menu_two(self):
        for ids, abbreviation, symbol in self.menu_list:
            self.dropdown_list.append(
                {'viewclass': 'OneLineListItem',
                 'text': f'{ids} - {abbreviation} - {symbol}',
                 'on_press': lambda x=f'{ids} - {symbol}': self.option_callback(x)}
            )
        self.menu = MDDropdownMenu(width_mult=4)
        self.menu.caller = self.ids.drop_item_two
        self.menu.items = self.dropdown_list
        self.menu.open()

    def option_callback(self, x):
        self.menu.caller.text = str(x)
        self.menu.dismiss()

    def get_exchange_rate(self, from_currency, to_currency):
        CurrencyManager().get_exchange_rate(from_currency, to_currency, self.on_rate_success, self.on_rate_failure)

    def on_rate_success(self, rate):
        self.rate = rate

    def on_rate_failure(self, error):
        self.rate = 0
        self.error = error

    def flip(self):
        if self.state == 0:
            self.state = 1
            self.ids.toolbar.title = 'From RSD to EUR'
            self.get_exchange_rate('RSD', 'EUR')
            self.ids.upper_label.text = ''
            self.ids.bottom_label.text = ''
            self.ids.input.text = ''
        else:
            self.state = 0
            self.ids.toolbar.title = 'From EUR to RSD'
            self.get_exchange_rate('EUR', 'RSD')
            self.ids.upper_label.text = ''
            self.ids.bottom_label.text = ''
            self.ids.input.text = ''

    def convert(self):
        if self.state == 0:
            try:
                customer_input = float(self.ids.input.text)
            except ValueError:
                self.ids.upper_label.text = f'Please enter the valid amount'
                self.ids.bottom_label.text = ''
                return
            one_eur = self.rate
            if self.rate == 0:
                self.ids.upper_label.theme_text_color = 'Error'
                self.ids.upper_label.text = self.error
                self.ids.bottom_label.text = ''
                return
            amount = round(customer_input * one_eur, 2)
            self.ids.upper_label.text = f'{self.ids.input.text} EUR is: '
            self.ids.bottom_label.text = f'{amount} RSD'

        else:
            try:
                customer_input = float(self.ids.input.text)
            except ValueError:
                self.ids.upper_label.text = f'Please enter the valid amount'
                self.ids.bottom_label.text = ''
                return
            one_din = self.rate
            if self.rate == 0:
                self.ids.upper_label.theme_text_color = 'Error'
                self.ids.upper_label.text = self.error
                self.ids.bottom_label.text = ''
                return

            amount = round(customer_input * one_din, 2)
            self.ids.upper_label.text = f'{self.ids.input.text} RSD is: '
            self.ids.bottom_label.text = f'{amount} EUR'

    def buy_money(self):
        from_value = self.ids.drop_item_one.text[:3]
        to_value = self.ids.drop_item_two.text[:3]
        if not from_value.isupper():
            result = 'Please choose FROM currency'
            self.ids.result.text = result
            return
        if not to_value.isupper():
            result = 'Please choose TO currency'
            self.ids.result.text = result
            return
        try:
            amount = float(self.ids.amount_input.text)
            multiplier = self.rate
            result = round(multiplier * amount, 2)
            self.ids.result.text = f'For {amount} {from_value}\n you get {result} {to_value}'
        except ValueError:
            result = 'Please enter the amount!'
            self.ids.result.text = result
        except Exception as e:
            print(e.args)
            result = 'Something went wrong. Try again'
            self.ids.result.text = result

    def get_rate(self):
        from_value = self.ids.drop_item_one.text[:3]
        to_value = self.ids.drop_item_two.text[:3]
        self.get_exchange_rate(from_value, to_value)


class ConverterApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'DeepOrange'
        return Builder.load_file('convert_me.kv')


if __name__ == '__main__':
    ConverterApp().run()
