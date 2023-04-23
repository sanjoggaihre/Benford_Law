from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import csv
import json
from benford import benford_fun

@view_config(
        route_name = 'start',
        renderer = 'templates/index.jinja2'
)
def initial_view(request):
    return {'title':'Benford Law'}


@view_config(
        route_name = 'checker',
        renderer = 'json'
        )
def benford(request):
    if request.method == 'POST' and request.POST['file'].file:
        csv_file = request.POST['file'].file
        filename = request.POST['file'].filename
        name , ext = filename.split('.')
        if not ext == 'csv':
            return {"The input form is not in csv format"}
        else:
            data = []
            reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
            for row in reader:
                data.extend(row)

            result = benford_fun(data)

            print (f'result is {result}')
            if result != None:
                with open("uploads/benford.json", 'w') as f:
                    json.dump(result,f)
                    result = Response(json.dumps(result))
                    return Response ("Data follows Benford Distribution")
            else:
                return Response ("Data doesn't follow Benford distribution")
        


if __name__ == '__main__':
    with Configurator() as config:
        config.include('pyramid_jinja2')
        config.add_static_view(name='static',path='static')
        config.include('pyramid_debugtoolbar')
        config.add_route('start', '/')
        config.add_route('checker', '/checker')
        config.scan()
        app = config.make_wsgi_app()

    
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()