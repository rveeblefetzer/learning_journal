from .security import TheRoot


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('login', '/login', factory=TheRoot)
    config.add_route('logout', '/logout', factory=TheRoot)
    config.add_route('homepage', '/', factory=TheRoot)
    config.add_route('write', 'journal/write', factory=TheRoot)
    config.add_route('detail', 'journal/{id:\d+}', factory=TheRoot)
    config.add_route('edit', 'journal/{id:\d+}/editentry', factory=TheRoot)
