import os
import sys

# Add the project directory to the sys.path
project_dir = '/home/yourusername/eventstack'  # Change this on PythonAnywhere
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

from main import make_app
import tornado.wsgi

application = tornado.wsgi.WSGIAdapter(make_app())
