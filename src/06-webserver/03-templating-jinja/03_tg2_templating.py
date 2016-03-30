__author__ = 'alexcomu'
from tg import AppConfig, TGController
from tg import expose

# We import the psutil library to retrieve our CPU usage
# and the json module to encode our usage data as a Javascript array
import psutil, json

class RootController(TGController):
    # If you pass a Template to the @expose decorator
    # each time the controller gets called it will render
    # that template. In this case we are rendering the
    # index.html template
    @expose('03_index.html')
    def index(self, **kw):
        # Every parameter we get from the browser
        # like /index?count=20 is available
        # inside the KW dictionary
        count = int(kw.get('count', 40))

        # We fetch enough CPU data every 100ms to create
        # a graph with at least count entries (by default 40)
        data = []
        for i in range(count):
            data.append(psutil.cpu_percent(interval=0.1))

        # Here we encode our Python list as a Javascript
        # array of numbers, if you try to print the jsdata
        # you will see that is the Javascript code for an array.
        # This way we can use it from our javascript script
        jsdata = json.dumps(data)

        # If you expose a template, the controller is required
        # to return a dictionary with inside any data
        # that has to be available to the template
        return dict(data=jsdata, num=len(data))


config = AppConfig(minimal=True, root_controller=RootController())

# Major change from step 0 is that we register the Jinja
# template engine so that we can render our index.html file
config.renderers = ['jinja']
config.default_renderer = 'jinja'

config.serve_static = True
config['paths']['static_files'] = '.'

from wsgiref.simple_server import make_server
print "Serving on port 8080..."
httpd = make_server('', 8080, config.make_wsgi_app())
httpd.serve_forever()