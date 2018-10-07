import os
import sys

from bson import ObjectId
from pymongo import MongoClient


class SpecialsSeeder:
    def __init__(self):
        host = os.getenv('DOC_STORE_HOST', 'doc-store')
        client = MongoClient(f'mongodb://{host}:27017/market')
        self.db = client.market

    def seed(self):
        print('Clearing collection...')
        self.db.specials.remove({})
        print('Inserting specials...')
        self.db.specials.insert_many(self.get_current_specials())
        print('Done.')

    def get_current_specials(self):
        return [
            dict(
                _id=ObjectId(),
                code='BOGO',
                description='Buy-One-Get-One-Free Special on Coffee.',
                limit=0,
                condition=dict(
                    CF1=2,
                ),
                reward=dict(
                    CF1=dict(
                        quantity=1,
                        change=1.0
                    ),
                )
            ),
            dict(
                _id=ObjectId(),
                code='APPL',
                description='If you buy 3 or more bags of Apples, the price drops to $4.50.',
                limit=1,
                condition=dict(
                    AP1=3,
                ),
                reward=dict(
                    AP1=dict(
                        quantity=0,
                        change=0.25
                    ),
                )
            ),
            dict(
                _id=ObjectId(),
                code='CHMK',
                description='Purchase a box of Chai and get milk free.',
                limit=1,
                condition=dict(
                    CH1=1,
                    MK1=1,
                ),
                reward=dict(
                    MK1=dict(
                        quantity=1,
                        change=1.0,
                    ),
                )
            ),
            dict(
                _id=ObjectId(),
                code='APOM',
                description='Purchase a bag of Oatmeal and get 50% off a bag of Apples.',
                limit=0,
                condition=dict(
                    OM1=1,
                    AP1=1,
                ),
                reward=dict(
                    AP1=dict(
                        quantity=1,
                        change=0.5
                    )
                )
            ),
        ]


SpecialsSeeder().seed()
sys.exit(0)
