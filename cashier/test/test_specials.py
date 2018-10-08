import os
import time

import requests

from app import specials


def test_determine_special_applies():

    condition = dict(CF1=2,)
    cart = ['CF1']
    result = specials.determine_special_applies(condition, cart)
    assert not result[0], "Expected cart:{cart} not to trigger {condition}"
    cart = ['CF1']*2
    result = specials.determine_special_applies(condition, cart)
    assert result[0], "Expected cart:{cart} to trigger {condition}"
    assert result[1] == ['CF1']*2, "Expected 'applied-to' be "

    condition = dict(AP1=3,)
    cart = ['AP1', ]*2
    result = specials.determine_special_applies(condition, cart)
    assert not result[0], "Expected cart:{cart} not to trigger {condition}"
    cart = ['AP1', ]*3
    result = specials.determine_special_applies(condition, cart)
    assert result[0], "Expected cart:{cart} to trigger {condition}"

    condition = dict(CH1=1, MK1=1,)
    cart = ['CH1', ]
    result = specials.determine_special_applies(condition, cart)
    assert not result[0], "Expected cart:{cart} not to trigger {condition}"
    cart = ['MK1', ]
    result = specials.determine_special_applies(condition, cart)
    assert not result[0], "Expected cart:{cart} not to trigger {condition}"
    cart = ['CH1', 'MK1', ]
    result = specials.determine_special_applies(condition, cart)
    assert result[0], "Expected cart:{cart} to trigger {condition}"

    condition = dict(OM1=1, AP1=1,)
    cart = ['OM1', ]
    result = specials.determine_special_applies(condition, cart)
    assert not result[0], "Expected cart:{cart} not to trigger {condition}"
    cart = ['AP1', ]
    result = specials.determine_special_applies(condition, cart)
    assert not result[0], "Expected cart:{cart} not to trigger {condition}"
    cart = ['OM1', 'AP1', ]
    result = specials.determine_special_applies(condition, cart)
    assert result[0], "Expected cart:{cart} to trigger {condition}"


def test_determine_reduction():
    """Verify percent reward change type"""
    price = 5.0
    value = 0.5
    expected = (price * value)
    result = specials.calculate_reduction(value, price)
    assert result == expected, 'Expected price reduction of {expected}, but got {result}'


def test_calculate_total():
    """Verify correct results of calculation"""
    products_service = os.getenv('PRODUCT_SERVICE_HOST')
    # health check
    for _ in range(3):
        r = requests.get(products_service + '/health-check')
        if r.status_code == 200:
            break
        time.sleep(3)
    products = requests.get('{0}/products'.format(products_service)).json()
    price = dict((p['code'], float(p['price'])) for p in products)
    items = [
        ('AP1', dict(price=price['AP1'],
                     specials=dict(APOM=dict(change=0.5, reduction=0), APPL=dict(change=0.25, reduction=0)))),
        ('AP1', dict(price=price['AP1'],
                     specials=dict(APOM=dict(change=0.5, reduction=0), APPL=dict(change=0.25, reduction=0)))),
        ('AP1', dict(price=price['AP1'], specials=dict(
            APPL=dict(change=0.25, reduction=0)))),
        ('CH1', dict(price=price['CH1'], specials=dict())),
        ('MK1', dict(price=price['MK1'], specials=dict(
            CHMK=dict(change=1.0, reduction=0)))),
        ('OM1', dict(price=price['OM1'], specials=dict())),
        ('OM1', dict(price=price['OM1'], specials=dict())),
        ('CF1', dict(price=price['CF1'], specials=dict(
            BOGO=dict(change=1.0, reduction=0)))),
        ('CF1', dict(price=price['CF1'], specials=dict())),
    ]
    intermediate = specials.calculate_reduction(0.25, price['AP1'])
    expected_total = sum([
        price['AP1'] - intermediate -
        specials.calculate_reduction(0.5, price['AP1'] - intermediate),
        price['AP1'] - intermediate -
        specials.calculate_reduction(0.5, price['AP1'] - intermediate),
        price['AP1'] - specials.calculate_reduction(0.25, price['AP1']),
        price['CH1'],
        price['MK1'] - specials.calculate_reduction(1.0, price['MK1']),
        price['OM1'],
        price['OM1'],
        price['CF1'] - specials.calculate_reduction(1.0, price['CF1']),
        price['CF1'],

    ])
    total, _ = specials.calculate_total(items)
    assert total == expected_total
