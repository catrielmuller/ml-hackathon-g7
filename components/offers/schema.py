offer_schema = {
    'meli_seller_id': {'type': 'string', 'required': True},
    'meli_item_id': {'type': 'string', 'required': True},
    'meli_link': {'type': 'string', 'required': True},
    'meli_image': {'type': 'string', 'required': True},
    'product': {'type': 'objectid', 'data_relation': {'resource': 'product', 'embeddable': True}},
    'original_price': {'type': 'number', 'required': True},
    'new_price': {'type': 'number', 'required': True}
}
