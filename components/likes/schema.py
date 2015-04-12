like_schema = {
    'user': {'type': 'objectid', 'data_relation': {'resource': 'user', 'embeddable': True}},
    'product': {'type': 'objectid', 'data_relation': {'resource': 'product', 'embeddable': True}},
    'does_like': {'type': 'boolean', 'required': True},
    'viewed': {'type': 'boolean', 'default': False}
}
