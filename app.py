from doctest import debug
from flask import Flask, app
from routes import routes

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "Vinnovate"

    app.register_blueprint(routes)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True,port= 6969)
