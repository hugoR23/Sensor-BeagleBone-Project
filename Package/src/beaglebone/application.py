'''
@Author: Hugo Robellaz
'''
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
import os

def main():
    config = Configurator()
    #Create the routes for the images
    config.add_route('mainPlot', '/mainPlot.png')
    config.add_route('smallPlot', '/smallPlot.png')
    #Request a scan of views.py for new routes
    config.scan("views")
    #Serve the static files (css, js, img...)
    config.add_static_view('static', 'static/',  cache_max_age=86400)
    app = config.make_wsgi_app()
    return app

def realmain():
    app = main()
    server = make_server('0.0.0.0', 8080, app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        #Delete the plot images at the end of a session
        filelist = [ f for f in os.listdir("./plots/") if f.endswith(".png") ]
        for f in filelist:
           os.remove('./plots/'+f)

if __name__ == '__main__':
    realmain()
