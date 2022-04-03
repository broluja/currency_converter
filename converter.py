from kivy.config import Config

Config.set("graphics", "width", "630")
Config.set("graphics", "height", "950")

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.behaviors import CoverBehavior
from kivy.uix.recycleview import RecycleView
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu

from currencies import exchange_rate, get_currencies

URL = "https://free.currconv.com/"
API_KEY = 'bfc0324d084dd91c0e6f'


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []
        self.get_data()

    def get_data(self):
        data = get_currencies()
        for name, currency in data:
            name = currency['currencyName']
            ids = currency['id']
            symbol = currency.get('currencySymbol', '')
            self.data.append({'text': f'{ids} - {name} - {symbol}', 'font_size': 24})


class MyLayout(BoxLayout):
    state = NumericProperty(0)
    recycleView = ObjectProperty(None)
    menu = ObjectProperty()

    def open_menu_one(self):
        menu_list = []
        data = get_currencies()
        for name, curr in data:
            abbreviation = curr['currencyName']
            ids = curr['id']
            symbol = curr.get('currencySymbol', '')
            menu_list.append(
                {'viewclass': 'OneLineListItem',
                 'text': f'{ids} - {abbreviation} - {symbol}',
                 'on_press': lambda x=f'{ids} - {symbol}': self.option_callback(x)}
            )
        self.menu = MDDropdownMenu(
            width_mult=4,
            caller=self.ids.drop_item_one,
            items=menu_list
        )
        self.menu.open()

    def open_menu_two(self):
        menu_list = []
        data = get_currencies()
        for _, curr in data:
            abbreviation = curr['currencyName']
            ids = curr['id']
            symbol = curr.get('currencySymbol', '')
            menu_list.append(
                {'viewclass': 'OneLineListItem',
                 'text': f'{ids} - {abbreviation} - {symbol}',
                 'on_press': lambda x=f'{ids} - {symbol}': self.option_callback(x)}
            )
        self.menu = MDDropdownMenu(
            width_mult=4,
            caller=self.ids.drop_item_two,
            items=menu_list
        )
        self.menu.open()

    def option_callback(self, x):
        self.menu.caller.text = str(x)
        self.menu.dismiss()

    def list_currencies(self):
        data = get_currencies()
        self.recycleView = data

    def flip(self):
        if self.state == 0:
            self.state = 1
            self.ids.toolbar.title = 'Convert from RSD to EUR'
            self.ids.upper_label.text = ''
            self.ids.bottom_label.text = ''
            self.ids.input.text = ''
        else:
            self.state = 0
            self.ids.toolbar.title = 'Convert from EUR to RSD'
            self.ids.upper_label.text = ''
            self.ids.bottom_label.text = ''
            self.ids.input.text = ''

    def convert(self):
        if self.state == 0:
            try:
                customer_input = float(self.ids.input.text)
            except ValueError:
                self.ids.upper_label.text = f'Please enter the valid amount'
                return
            one_eur = exchange_rate('EUR', 'RSD')
            amount = round(customer_input * one_eur, 2)
            self.ids.upper_label.text = f'{self.ids.input.text} EUR is: '
            self.ids.bottom_label.text = f'{amount} RSD'

        else:
            try:
                customer_input = float(self.ids.input.text)
            except ValueError:
                self.ids.upper_label.text = f'Please enter the valid amount'
                return
            one_din = exchange_rate('RSD', 'EUR')
            amount = round(customer_input * one_din)
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
            multiplier = exchange_rate(from_value, to_value)
            result = round(multiplier * amount, 2)
            self.ids.result.text = f'For {amount} {from_value}\n you get {result} {to_value}'
        except ValueError:
            result = 'Please enter the amount!'
            self.ids.result.text = result
        except Exception as e:
            print(e.args)
            result = 'Something went wrong. Try again'
            self.ids.result.text = result


class ConverterApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'DeepOrange'
        return Builder.load_file('convert_me.kv')


if __name__ == '__main__':
    ConverterApp().run()
