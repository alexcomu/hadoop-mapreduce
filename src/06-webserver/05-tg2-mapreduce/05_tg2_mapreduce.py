__author__ = 'alexcomu'
from tg import AppConfig, TGController
from tg import expose

from mrjob.protocol import JSONValueProtocol
from wordcount import MRWordFreqJSON
from text import TEXT


class RootController(TGController):
    @expose('05_index.html')
    def index(self, **kw):
        return dict()

    @expose('json', content_type='application/json')
    def data(self, minimum=1, **kw):
        res = []

        mr_job = MRWordFreqJSON()
        mr_job.stdin = [JSONValueProtocol().write(None, line) for line in TEXT]

        with mr_job.make_runner() as runner:
            runner.run()
            for line in runner.stream_output():
                key, value = mr_job.parse_output_line(line)
                if int(value) >= int(minimum):
                    res.append([key, value])

        return dict(data=res)


config = AppConfig(minimal=True, root_controller=RootController())

config.renderers = ['json', 'jinja']
config.default_renderer = 'jinja'

config.serve_static = True
config['paths']['static_files'] = './'

from wsgiref.simple_server import make_server
print "Serving on port 8080..."
httpd = make_server('', 8080, config.make_wsgi_app())
httpd.serve_forever()