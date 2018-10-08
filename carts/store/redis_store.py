import uuid
from datetime import timedelta

import redis
from store.store import Store as BaseStore


class Store(BaseStore):

    TTL = timedelta(days=1)

    def __init__(self, *args, **kwargs):
        self.conn = redis.StrictRedis(host=kwargs.get('host', 'redis'))

    def get_cart(self, id):
        """Retrieve a cart by ID"""
        return dict(id=id, items=self._get(id))

    def update_cart(self, id=None, add=dict(), remove=dict()):
        """
        Add and/or remove elements from the list store
        If id is None, one is generated.
        If add and remove are both None, id is returned, but nothing is stored
        """
        print(id, add, remove)
        id = self._cart_id() if id is None else id
        for a, quantity in add.items():
            print('push', a, quantity)
            self.conn.rpush(id, *([a]*quantity))
        for r, quantity in remove.items():
            print('rem', r, quantity)
            self.conn.lrem(id, quantity, r)
        self.conn.expire(id, self.TTL)
        items = self._get(id)
        print(items)
        return dict(id=id, items=items)

    def delete_cart(self, id):
        """Remove a cart manually"""
        self.conn.delete(id)

    def health_check(self):
        """Verifies the store health"""
        try:
            self.conn.ping()
        except redis.exceptions.ConnectionError:
            return False
        return True

    def _get(self, id):
        """Simple Retrieval of entire cart"""
        return list(x.decode() for x in self.conn.lrange(id, 0, -1))

    @staticmethod
    def _cart_id():
        """Generate Cart ID"""
        return uuid.uuid4().hex
