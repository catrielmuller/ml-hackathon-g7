product_schema = {
    'product_id': {'type': 'string', 'required': True},
    'image_url': {'type': 'string'},
    'description': {'type': 'string'},
    'category': {'type': 'objectid', 'data_relation': {'resource': 'category', 'embeddable': True}}
}
