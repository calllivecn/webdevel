
from flask import Flask
from asgiref.wsgi import WsgiToAsgi

app = Flask("test")

@app.route("/")
def hello_world():
        return "<p>Hello, World!</p>"


asgi_app = WsgiToAsgi(app)

if __name__ == "__main__":
    app.run()

