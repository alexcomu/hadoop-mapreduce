__author__ = 'alexcomu'
from tg import AppConfig, TGController
from tg import expose

import psutil

class RootController(TGController):
    @expose('04_index.html')
    def index(self, **kw):
        # As our data is now provided on realtime
        # by the "data" controller method, our index
        # doesn't have to send anything to the template
        # which is just going to be initialized with a
        # bunch of 0.
        #
        # You will notice that 'n' and 'data' got also
        # removed from our index.html template
        return dict()

    # Here we tell to TurboGears to get the result provided
    # by our controller method and encode it as JSON so
    # that we can load it back using d3.json from javascript
    @expose('json', content_type='application/json')
    def data(self, **kw):
        #We just return an 'usage' value with the current
        #CPU usage percentage.
        return dict(usage=psutil.cpu_percent(interval=0.1))


config = AppConfig(minimal=True, root_controller=RootController())

#Only change since before is that we register the 'json' renderer
#into our list of available renderers, so that we are able to
#encode our responses as JSON
config.renderers = ['json', 'jinja']
config.default_renderer = 'jinja'

config.serve_static = True
config['paths']['static_files'] = './'

from wsgiref.simple_server import make_server
print "Serving on port 8080..."
httpd = make_server('', 8080, config.make_wsgi_app())
httpd.serve_forever()
