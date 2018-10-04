import os

from store.redis_store import Store


def test_store_get():
    store = Store(host=os.getenv('CART_STORE_HOST', 'cart-store'))

    result = store.update_cart(id=None, add={
        'AP1': 4,
        'CH1': 2,
    }, remove={
        'AP1': 1,
        'CH1': 1,
    })

    print(result)
    assert 'cart' in result, 'Expected "cart" in result from store'
    assert 'id' in result, 'Expected "cart" in result from store'
    ap1 = [x for x in result['cart'] if x == 'AP1']
    ap1_count = len(ap1)
    ch1 = [x for x in result['cart'] if x == 'CH1']
    ch1_count = len(ch1)
    assert ap1_count == 3, 'Expected 3 AP1, but got {0} - {1}'.format(
        ap1_count, ap1)
    assert ch1_count == 1, 'Expected 1 CH1, but got {0} - {1}'.format(
        ch1_count, ch1)
