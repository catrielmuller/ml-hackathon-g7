from .schema import user_schema


RESOURCES = [{
    'name': 'user',
    'domain_settings': {
        'schema': user_schema,
    },
}]
