def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('homepage', '/')
    config.add_route('write', 'journal/write')
    config.add_route('detail', 'journal/{id:\d+}')
    config.add_route('edit', 'journal/{id:\d+}/editentry')
