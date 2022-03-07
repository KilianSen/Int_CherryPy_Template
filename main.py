from site_loader import load_site

import os
import cherrypy
import ppi.CAuth as CAuth


class Page(object):
    def dynamic_expose(self, loc: str, name: str) -> bool:

        @cherrypy.expose(name)
        @CAuth.CherrySecurity.auth_required()
        @load_site(loc)
        def proto_function(html_data):
            cherrypy.log(f"[dyn] Serving page {name} from {loc} with the proto_function")
            return html_data

        if not hasattr(self, name):
            cherrypy.log(f"[dyn] Automatically exposed {loc} as {name} using proto_function")
            setattr(self, name, proto_function)
            return True

        cherrypy.log(f"[dyn] Couldn´t expose {loc} as {name} using proto_function")
        return False

    def __init__(self):
        for file in os.listdir('static/pages/'):
            self.dynamic_expose('static/pages/' + file, file.split('.')[0])

    @cherrypy.expose
    @load_site(location='static/pages/index.html')
    def index(self, html_data):
        return html_data

    @cherrypy.expose
    @load_site(location='static/pages/login.html')
    def login(self, html_data, **kwargs):
        if 'username' in kwargs:
            username: str = kwargs['username']
            password: str = kwargs['password']
            if 'login' in kwargs:
                CAuth.CherrySecurity.login(username, password)
            if 'register' in kwargs:
                CAuth.CherrySecurity.register(username, password)
        return html_data


if __name__ == '__main__':
    cherrypy.server.socket_host = '0.0.0.0'
    root_dir = os.path.abspath(os.path.dirname(__file__))
    conf = {'/static': {'tools.staticdir.on': True,
                        'tools.staticdir.dir': f'{root_dir}/static'}}
    cherrypy.config.update({
        'global': {
            'engine.autoreload.on': False
        }
    })
    cherrypy.quickstart(Page(), config=conf)
