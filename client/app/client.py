import json

import requests


class Client:
    """Farmer's Market API Client"""

    def __init__(self, protocol='https', service_host='api', service_port='5000'):
        self.service_url = protocol + '://' + service_host + ':' + service_port
        self.cart_id = None

    def commands(self):
        return (
            "Welcome to The Farmer's Market!",  # self.products(),
            'Commands:',
            '\tproducts : List the available products',
            '\t<product code>[,...] : Add products to cart',
            '\tinvoice : Show the detailed invoice',
            '\tnew : Empty the current Cart',
            '\texit : Close the market app',
            '\t<empty prompt> : Show these commands',
            )

    def start(self):
        """Start handling input in the interaction loop"""
        output(self.products())
        output(self.commands())
        while True:
            print('>>>', end=' ')
            try:
                output(self.handle(input()))
            except SignalExit as s:
                print(s)
                break
            except Signal as s:
                print(s)

    def handle(self, command):
        """Handle a command input and return a response list"""
        if command == 'exit':
            # stop the client
            raise SignalExit("Thank you for your patronage")
        elif command == 'new':
            # clear the cart
            self.new_cart()
            return ('Created a new cart', self.current_cart())
        elif command == 'invoice':
            # toggle detailed invoice mode
            return self.current_cart(invoice=True)
        elif command == 'products':
            # show the product table
            return self.products()
        elif command == '':
            return self.show_commands()
        else:
            # presume one or more items to add
            self.add_item(command)
            return ('Updated cart', self.current_cart())

    def new_cart(self, items=()):
        """Empty the current cart by creating a new one"""
        # TODO: Post cart + items
        r = requests.post('/'.join((self.service_url, 'cart', )), data=json.dumps(items))
        # TODO: Store cart ID
        self.cart_id = json.loads(r.json())['id']

    def current_cart(self, invoice=False):
        """
        Format the simplified cart + total, specials applied.
        :param invoice: Show the itemized register invoice
        :return: string
        """
        url = '/'.join((self.service_url, 'cart', self.cart_id))
        if invoice:
            url = '/'.join((url, 'invoice'))
        r = requests.get(
            url,
            params={'invoice': invoice}
        )
        result = json.loads(r.json())
        return result

    def add_item(self, input_str):
        """Add items to the cart"""
        if input_str is None or input_str == '':
            return

        items = input_str.split(',')
        print(input_str, "->", items)

        if self.cart_id is None:
            self.new_cart(items=items)
        else:
            requests.put('/'.join((self.service_url, 'cart')), data=json.dumps(items))

    def products(self):
        """Return the products table"""
        r = requests.get('/'.join((self.service_url, 'products')))
        # TODO: Format the products table as a multi-line string
        json.loads(r.json())
        return ""


# Signal for communicating to the application loop
class Signal(Exception):
    pass


class SignalExit(Signal):
    pass


def output(it):
    """Output an iterable on separate lines"""
    if it:
        print('\n'.join(it))
