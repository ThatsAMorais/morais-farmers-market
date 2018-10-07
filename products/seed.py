import sys

from app.products import Product, db

from sqlalchemy.exc import OperationalError


class ProductsSeeder:

    def __init__(self):
        # While trivial, the structure of this seeder is designed to do setup here, invocation later
        self.db = db

    def health_check(self):
        # Health Check
        while True:
            try:
                self.db.engine.execute('SELECT 1')
            except OperationalError:
                continue
            break

    def seed(self):
        print('Verify DB Connection')
        self.health_check()
        print('Dropping tables...')
        self.db.drop_all()
        print('Creating tables...')
        self.db.create_all()
        print('Inserting products...')
        self.db.session.add(Product(code='CH1', name='Chai', price='3.11'))
        self.db.session.add(Product(code='AP1', name='Apples', price='6.00'))
        self.db.session.add(Product(code='CF1', name='Coffee', price='11.23'))
        self.db.session.add(Product(code='MK1', name='Milk', price='4.75'))
        self.db.session.add(Product(code='OM1', name='Oatmeal', price='3.69'))
        self.db.session.commit()
        print('Done.')


ProductsSeeder().seed()
sys.exit(0)
