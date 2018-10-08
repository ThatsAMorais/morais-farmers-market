import json
import time
import requests
from collections import defaultdict


class Client:
    """Farmer's Market API Client"""

    def __init__(self, service_host='market-api'):
        self.service_url = service_host
        self.cart_id = None

    def commands(self):
        return (
            'Commands:',
            '\tproducts : List the available products',
            '\tspecials : List ongoing specials',
            '\t<product code>[,...] : Add products to cart',
            '\tinvoice : Show the detailed invoice',
            '\tnew : Empty the current Cart',
            '\texit : Close the market app',
            '\t<empty prompt> : Show these commands',
        )

    def start(self):
        """Start handling input in the interaction loop"""

        # Dependency Health Check
        self.health_check()
        print("Welcome to The Farmer's Market!")
        output(self.products())
        output(self.specials())
        self.new_cart()
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
            return self.current_cart()
        elif command == 'invoice':
            # toggle detailed invoice mode
            return self.current_cart(invoice=True)
        elif command == 'products':
            # show the product table
            return self.products()
        elif command == 'specials':
            return self.specials()
        elif command == '':
            return self.commands()
        else:
            # presume one or more items to add
            self.add_item(command)
            return self.current_cart()

    def new_cart(self):
        """Empty the current cart by creating a new one"""
        r = requests.post(self.service_url + '/carts')
        self.cart_id = r.json()['cart']['id']

    def current_cart(self, invoice=False):
        """
        Format the simplified cart + total, specials applied.
        :param invoice: Show the itemized register invoice
        :return: string
        """
        width = 35

        def get_data():
            url = self.service_url + '/cart/' + self.cart_id
            if invoice:
                url += '/invoice'

            # Setup a small retry loop for a smooth client experience with remote systems
            for _ in range(3):
                r = requests.get(url)
                if r.status_code == 200:
                    return r
                break
            return None

        def gen_output(resp):
            if invoice:
                cart_output = [
                    '{0}{1}'.format('Item'.ljust(width//2, ' '),
                                    'Price'.rjust(width//2, ' ')),
                    '{0}{1}'.format('----'.ljust(width//2, ' '),
                                    '-----'.rjust(width//2, ' '))
                ]
                for (product_code, details) in (resp.json()['invoice']['items']) if resp else ():
                    cart_output.append('{0}{1}'.format(product_code.ljust(width//2, ' '),
                                                       ('{:,.2f}'.format(details['price'])).rjust(width//2, ' ')))
                    for (sp_code, d) in sorted([(sp_code, sp) for sp_code, sp in details['specials'].items()],
                                               key=lambda r: r[1]['change']):
                        cart_output.append(
                            '{0}{1}'.format(sp_code.rjust(width//2, ' '),
                                            '{:,.2f}'.format(-d['reduction']).rjust(width//2, ' ')))
                if resp:
                    total = resp.json()['invoice']['total']
                else:
                    total = 0.0
                cart_output.extend([
                    ''.rjust(width, '-'),
                    '{:,.2f}'.format(total).rjust(width, ' ')
                ])
                return cart_output

            cart_output = [
                'Basket: ' + ', '.join(resp.json()['cart']['items']),
                'Total: ${:,.2f}'.format(resp.json()['total']),
            ]
            return cart_output

        resp = get_data()
        if None:
            output = ['Service failure: please try again']
        else:
            output = gen_output(resp)
        return output

    def add_item(self, input_str):
        """Add items to the cart"""

        items = defaultdict(int)
        for x in input_str.replace(' ', '').split(','):
            items[x] += 1
        requests.post(self.service_url + '/cart/' +
                      self.cart_id, data=json.dumps(dict(add=items)))

    def products(self):
        """Return the products table"""
        r = requests.get(self.service_url + '/products')
        if r.status_code != 200:
            products = []
        else:
            products = r.json()['products']
        product_output = [
            '+--------------|--------------|---------+',
            '| Product Code |     Name     |  Price  |',
            '+--------------|--------------|---------+',
        ]
        product_output.extend(['|{0: ^14}|{1: ^14}|{2: ^8}|'.format(
            line['code'], line['name'], '${:,.2f}'.format(line['price'])) for line in products])
        product_output.append('+--------------|--------------|---------+')
        return product_output

    def specials(self):
        # TODO: Dynamic rendering of currently available specials from cashier service
        return [
            ''.rjust(80, '-'),
            'Specials:',
            '-----',
            '1. BOGO -- Buy-One-Get-One-Free Special on Coffee. (Unlimited)',
            '2. APPL -- If you buy 3 or more bags of Apples, the price drops to $4.50.',
            '3. CHMK -- Purchase a box of Chai and get milk free. (Limit 1)',
            '4. APOM -- Purchase a bag of Oatmeal and get 50% off a bag of Apples',
            '          '.center(80, '-'),
            'Any doubly-applied specials are applied in increasing order of discount!',
            ''.rjust(80, '-'),
        ]

    def health_check(self):
        """Checks the health of the services on which this client depends"""
        print('Connecting with market service.', end='')
        while True:
            try:
                r = requests.get(self.service_url + '/health-check')
                if r.status_code != 200:
                    print('.', end='')
                    time.sleep(3)
                    continue
            except requests.exceptions.ConnectionError:
                print('.', end='')
                time.sleep(3)
                continue
            break
        print('. Ready!')


# Signal for communicating to the application loop
class Signal(Exception):
    pass


class SignalExit(Signal):
    pass


def output(it):
    """Output an iterable on separate lines"""
    if it:
        print('\n'.join(it))
