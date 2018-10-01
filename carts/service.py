"""
A service to provide Carts
"""
import os
import redis

r = redis.Redis(
    url='rediss://{0}:{1}'.format(os.getenv()),
    password='password', 
    )


def get_cart(self, cart_id=None):
    """Get a cart"""
    pass


def add_items(self, cart_id, **items):
    """Add items to a cart, where `items` is {product_code: quantity, ...}"""
    pass


def remove_items(self, cart_id, **items):
    """Remove items from a cart, where `items` is {product_code: quantity, ...}"""
    pass
