user_schema = {
    'meli_id': {'type': 'string', 'required': True},
    'email': {'type': 'string', 'required': True},
    'preferences': {
        'default': [],
        'type': 'list',
        'schema': {'type': 'objectid', 'data_relation': {'resource': 'category', 'embeddable': True}}
    }
}
