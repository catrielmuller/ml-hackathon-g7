offer_schema = {
    'seller': {'type': 'objectid', 'data_relation': {'resource': 'user', 'embeddable': True}},
    'item_id': {'type': 'string', 'required': True},
    'product_id': {'type': 'string', 'required': True},
    'price': {'type': 'string', 'required': True}
}
