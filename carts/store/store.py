

class Store(object):
    """Store Interface"""

    def get_cart(self, id):
        """Retrieve a cart by id, i.e. (id, ("1", "2", "3"))"""
        raise NotImplementedError('Must implement get_cart')

    def update_cart(self, id, add=(), remove=()):
        """Update a cart"""
        raise NotImplementedError('Must implement put_cart')

    def delete_cart(self, id):
        """Remove a cart manually"""
        raise NotImplementedError('Must implement delete_cart')

    def get_invoice(self, id):
        """Retrieve a cart invoice if it exists, else None"""
        raise NotImplementedError('Must implement get_invoice')

    def set_invoice(self, id, invoice):
        """Set a cart invoice"""
        raise NotImplementedError("Must implement set_invoice")
