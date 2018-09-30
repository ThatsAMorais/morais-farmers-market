"""
Verifies available Client CLI features. Good thing `Client.handle` was written in a testable way.
"""

from app.client import Client, SignalExit


def test_client_handle_exit():
    try:
        Client().handle("exit")
    except SignalExit as e:
        pass
    else:
        assert False, "Expected exit signal did not happen"


def test_client_handle_create_new_cart():
    result = Client().handle('new')
    assert len(result) == 2, "expected 2 strings, but got {0}".format(len(result))


def test_client_handle_get_invoice():
    result = Client().handle('invoice')
    assert len(result) > 0, "expected > 0 strings"


def test_client_handle_get_products():
    result = Client().handle('products')
    assert len(result) > 0, "expected > 0 strings"


def test_client_handle_add_item():
    result = Client().handle('anything')
    assert len(result) == 2, "expected 2 strings, but got {0}".format(len(result))
