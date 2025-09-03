"""Functions to manage a users shopping cart items."""


def add_item(current_cart, items_to_add):
    """Add items to shopping cart.

    :param current_cart: dict - the current shopping cart.
    :param items_to_add: iterable - items to add to the cart.
    :return: dict - the updated user cart dictionary.
    """
    for i in items_to_add:
        if i in current_cart:
            current_cart[i] += 1
        else:
            current_cart[i] = 1
    return current_cart

def read_notes(notes):
    """Create user cart from an iterable notes entry.

    :param notes: iterable of items to add to cart.
    :return: dict - a user shopping cart dictionary.
    """
    cart = {}
    
    for i in notes:
        if i in cart:
            cart[i] += 1
        else:
            cart[i] = 1
    return cart


def update_recipes(ideas, recipe_updates):
    """Update the recipe ideas dictionary.

    :param ideas: dict - The "recipe ideas" dict.
    :param recipe_updates: iterable -  with updates for the ideas section.
    :return: dict - updated "recipe ideas" dict.
    """

    for recipe_name, recipe_data in recipe_updates:  
        ideas[recipe_name] = recipe_data            
    return ideas


def sort_entries(cart):
    """Sort a users shopping cart in alphabetically order.

    :param cart: dict - a users shopping cart dictionary.
    :return: dict - users shopping cart sorted in alphabetical order.
    """
    new_dict = dict(sorted(cart.items()))
    return new_dict
    


def send_to_store(cart, aisle_mapping):
    """Combine users order to aisle and refrigeration information.

    :param cart: dict - users shopping cart dictionary.
    :param aisle_mapping: dict - aisle and refrigeration information dictionary.
    :return: dict - fulfillment dictionary ready to send to store.
    """
    if not isinstance(cart, dict):
        raise TypeError("cart must be a dictionary")
    if not isinstance(aisle_mapping, dict):
        raise TypeError("aisle_mapping must be a dictionary")

    fulfillment_cart = {}
    
    for item, quantity in cart.items():
        if item in aisle_mapping:
            if not isinstance(aisle_mapping[item], (list, tuple)) or len(aisle_mapping[item]) != 2:
                raise ValueError(f"aisle_mapping[{item}] must be a list or tuple with [aisle, refrigerated]")
            fulfillment_cart[item] = [quantity, aisle_mapping[item][0], aisle_mapping[item][1]]
        else:
            fulfillment_cart[item] = [quantity, 'Unknown', False]
    
    sorted_fulfillment_cart = dict(sorted(fulfillment_cart.items(), key=lambda x: x[0], reverse=True))
    
    return sorted_fulfillment_cart


def update_store_inventory(fulfillment_cart, store_inventory):
    """Update store inventory levels with user order.

    :param fulfillment cart: dict - fulfillment cart to send to store.
    :param store_inventory: dict - store available inventory
    :return: dict - store_inventory updated.
    """
    inventory_dict = {entry[0]: entry[1] for entry in store_inventory}

    updated_inventory = store_inventory.copy()

    for item, details in fulfillment_cart.items():
        qty_ordered = details[0]

        if item in updated_inventory:
            current_qty = updated_inventory[item][0]
            new_qty = current_qty - qty_ordered
            updated_inventory[item][0] = new_qty if new_qty > 0 else "Out of Stock"
        else:
            # item not in inventory
            updated_inventory[item] = ["Out of Stock"] + details[1:]

    return updated_inventory