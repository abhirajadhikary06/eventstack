from flask import Flask

app = Flask(__name__)  # 👈 This needs to be top-level

@app.route("/")
def index():
    return "Hello from PythonAnywhere!"
from app import app as application
path = '/home/sushritasingh01/eventstack'
@app.route("/wsgi-check")
def wsgi_check():
    return "WSGI setup is working!"