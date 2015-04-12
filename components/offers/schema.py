offer_schema = {
    'seller': {'type': 'objectid', 'data_relation': {'resource': 'user', 'embeddable': True}},
    'item_id': {'type': 'string', 'required': True},
    'product': {'type': 'objectid', 'data_relation': {'resource': 'product', 'embeddable': True}},
    'price': {'type': 'number', 'required': True}
}
