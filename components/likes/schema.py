like_schema = {
    'user': {'type': 'objectid', 'data_relation': {'resource': 'user', 'embeddable': True}},
    'product': {'type': 'objectid', 'data_relation': {'resource': 'product', 'embeddable': True}},
    'like': {'type': 'boolean', 'required': True},
}
