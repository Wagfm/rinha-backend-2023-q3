from flask import Flask

from controllers.persons import PersonsController
from routes.persons import PersonsRoute

app = Flask(__name__)
controller = PersonsController()
route = PersonsRoute("persons_route", controller)
app.register_blueprint(route)
