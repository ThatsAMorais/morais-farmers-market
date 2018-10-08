"""
Verifies available Client CLI features. Good thing `Client.handle` was written in a testable way.
"""
import os

from app.client import Client, SignalExit


def get_client():
    client = Client(service_host=os.getenv('MARKET_SERVICE_HOST'))
    # health check
    client.health_check()
    return client


def test_client_handle_exit():
    try:
        get_client().handle("exit")
    except SignalExit as e:
        pass
    else:
        assert False, "Expected exit signal did not happen"


def test_client_handle_create_new_cart():
    result = get_client().handle('new')
    assert len(result) == 2, "expected 2 strings, but got {0}".format(
        len(result))


def test_client_handle_get_invoice():
    client = get_client()
    client.new_cart()
    result = client.handle('invoice')
    assert len(result) > 0, "expected > 0 strings"


def test_client_handle_get_products():
    client = get_client()
    client.new_cart()
    result = client.handle('products')
    assert len(result) > 0, "expected > 0 strings"


def test_client_handle_add_item():
    client = get_client()
    client.new_cart()
    result = client.handle('AP1, CF1')
    assert len(result) == 2, "expected 2 strings, but got {0}".format(
        len(result))


def test_client_handle_add_item_invalid():
    client = get_client()
    client.new_cart()
    result = client.handle('anything')
    assert len(result) == 2, "expected 2 strings, but got {0}".format(
        len(result))
