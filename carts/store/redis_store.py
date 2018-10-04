import json
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
        return dict(id=id, cart=self._get(id))

    def update_cart(self, id=None, add=dict(), remove=dict()):
        """
        Add and/or remove elements from the list store
        If id is None, one is generated.
        If add and remove are both None, id is returned, but nothing is stored
        """
        id = self._cart_id() if id is None else id
        for a, quantity in add.items():
            self.conn.rpush(id, *([a]*quantity))
        for r, quantity in remove.items():
            self.conn.lrem(id, quantity, r)
        self.conn.expire(id, self.TTL)
        return dict(id=id, cart=self._get(id))

    def delete_cart(self, id):
        """Remove a cart manually"""
        self.conn.delete(id)
        self.conn.delete('invoice:' + id)

    def get_invoice(self, id):
        """Retrieve a cart invoice if it exists, else None"""
        if id is None:
            return None
        jsn = self.conn.get(self._invoice_id(id))
        return jsn if jsn is None else json.loads(jsn)

    def _get(self, id):
        """Simple Retrieval of entire cart"""
        return list(x.decode() for x in self.conn.lrange(id, 0, -1))

    def set_invoice(self, id, invoice):
        """Store a cached invoice"""
        self.conn.set(self._invoice_id(id), json.dumps(invoice))
        self.conn.expire(self._invoice_id(id), self.TTL)

    def delete_invoice(self, id):
        """Remove a cached invoice"""
        self.conn.delete(self._invoice(id))

    @staticmethod
    def _cart_id():
        """Generate Cart ID"""
        return uuid.uuid4().hex

    @staticmethod
    def _invoice_id(id):
        """Generate Cart Invoice ID"""
        return 'invoice:' + id
