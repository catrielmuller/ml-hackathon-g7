import pymongo
from settings import EVE_SETTINGS


def initialize_components(eve_app, components):
    """Initialize components' resources with the Eve app.  Accepts a single item or a list of them.  Each item must be
    a package with a variable called RESOURCES, which is a list of dictionaries, each containing the configuration
    information for a resource."""
    components = components if isinstance(components, (list, tuple)) else [components]
    for component in components:
        for resource in component.RESOURCES:
            _initialize_resource(eve_app, resource)


def _initialize_resource(eve_app, resource):
    """Register a resourcesce and its event callbacks with the Eve app (after initializing any components the resource
    depends on)"""
    name = resource['name']
    if name not in eve_app.config['DOMAIN']:
        initialize_components(eve_app, resource.get('dependencies', []))
        eve_app.register_resource(name, resource['domain_settings'])
        _register_event_callbacks(eve_app, name, resource.get('event_callbacks', {}))
        _ensure_indexes(name, resource.get('indexes', []))


def _register_event_callbacks(eve_app, resource_name, event_callbacks):
    """Register callbacks for Eve events to do with the resource"""
    for event, callback in event_callbacks.iteritems():
        full_event_name = "on_{}_{}".format(event, resource_name)
        # Eve events are supposed to be used like "eve_app.on_even_name += callback".  However, our event name is a
        # string, so we have to use this ugly workaround.  See https://github.com/nicolaiarocci/events/ for info
        event_slot = getattr(eve_app, full_event_name)
        event_slot.__iadd__(callback)


def _ensure_indexes(resource_name, indexes):
    client = pymongo.MongoClient(EVE_SETTINGS['MONGO_URI'])
    db = client[EVE_SETTINGS['MONGO_DBNAME']]
    for index, options in indexes:
        db[resource_name].ensure_index(index, **options)
