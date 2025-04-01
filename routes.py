from sys import flags
from flask import Blueprint , render_template
import flask

routes = Blueprint('routes' , __name__)

@routes.route('/')
def cre():
    return 'hi'