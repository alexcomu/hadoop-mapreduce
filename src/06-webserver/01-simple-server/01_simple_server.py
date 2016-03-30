__author__ = 'alexcomu'
# WSGI Introduction
# The wsgiref.simple_server provides a basic HTTP server
# which we can use to serve our Python WSGI Web Applications
from wsgiref.simple_server import make_server

# A minimum WSGI application consists of a callable
# which gets two arguments: The applicatio environment
# and a start_response function that can be called to
# start sending data back to the browser
def simple_application(environ, start_response):
    # Here we say to the browser that everything is fine
    # and we are going to send him the data
    start_response('200 OK', [])

    # Everything we return from our callable is
    # what we are going to see in our browser
    return ['Hello World']

def application_environment(environ, start_response):
    start_response('200 OK', [])
    resp = []
    for key, value in environ.items():
        resp.append('%s = %s\n' % (key, value))
    return resp

# Here we just create the HTTP Server and make it
# serve our web application on port 8080
print "Serving on port 8080..."
httpd = make_server('', 8080, application_environment)
httpd.serve_forever()
