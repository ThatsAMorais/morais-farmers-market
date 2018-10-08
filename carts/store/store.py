

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

    def health_check(self):
        """Verifies the store health"""
