like_schema = {
    'user': {'type': 'objectid', 'data_relation': {'resource': 'user', 'embeddable': True}},
    'product_id': {'type': 'string', 'required': True},
    'like': {'type': 'boolean', 'required': True},
}
