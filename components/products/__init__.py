from .schema import product_schema


RESOURCES = [{
    'name': 'product',
    'domain_settings': {
        'schema': product_schema,
    },
}]
