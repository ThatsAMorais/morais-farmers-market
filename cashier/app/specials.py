

# TODO: Organize into an invoice class?


def apply_specials(specials, cart, product_prices):
    """
    Apply specials to a set of products in a cart

    Expects:
    - specials: See seed.py
    - cart: [product-code, ...]
    - product_prices: dict(code=price, ...)
    """
    # Create an itemized invoice of items, but only for items in product_prices
    #  Technically, a cart doesn't care what you put in it, and its merely an
    #  option to guard against that for any users of this or the cart service.
    #  This service MUST, however, avoid tallying non-products in the cart.
    items = [(item, dict(price=product_prices[item], specials=dict()))
             for item in cart if item in product_prices]
    for sp in specials:
        times_applied = 0
        remaining_cart = list(cart)
        while (len(remaining_cart) > 0):
            # If requirements met on what remains in temp cart, apply special
            special_applies, applied_to = determine_special_applies(
                sp['condition'], remaining_cart)
            if not special_applies:
                break

            times_applied += 1

            # Update temp cart
            for a in applied_to:
                remaining_cart.remove(a)

            # Apply Reward
            items = apply_reward(
                sp['code'], sp['reward'], items, product_prices)

            # Break at the reward's limit
            if times_applied == sp['limit']:
                break

    total, items = calculate_total(items)
    return items, max(total, 0.0)


def determine_special_applies(condition, cart_items):
    """Based on the given cart, determine if the given condition applies"""
    applied_to = []
    for i, q in condition.items():
        if q <= cart_items.count(i):
            applied_to.extend([i]*q)
        else:
            return False, []
    return True, applied_to


def apply_reward(reward_code, reward, items, product_prices):
    """Apply the rewards to the cart"""
    for upc, r in reward.items():
        # Determine the price reduction
        quantity_applied = 0
        # Iterating over applicable items, attempt to apply the reward
        for a in [x for x in items if x[0] == upc]:
            if reward_code not in a[1]['specials']:
                a[1]['specials'][reward_code] = dict(
                    change=r['change'], reduction=0)
                quantity_applied += 1
                # Bound the application of the reward to its defined quantity
                if quantity_applied == r['quantity']:
                    break
    return items


def calculate_total(items):
    """Generate a final total including applied specials"""
    total = 0
    for (item, details) in items:
        amount = details['price']
        # Calculate modifications based on rewards from specials, from least to greatest
        for sp in sorted([sp for _, sp in details['specials'].items()],
                         key=lambda r: r['change']):
            reduction = calculate_reduction(sp['change'], amount)
            amount -= reduction
            sp['reduction'] = reduction
        # Regardless of the accuracy of the application, a special will
        # never enable the cashier to pay for a customer to buy an item
        total += max(0, amount)
    return total, items


def calculate_reduction(change, price):
    """Determine the price reduction"""
    return price * change
