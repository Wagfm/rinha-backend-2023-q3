import logging

from flask import Flask

from controllers.persons import PersonsController
from routes.persons import PersonsRoute

app = Flask(__name__)
app.logger.disabled = True
logging.getLogger("werkzeug").disabled = True
logging.getLogger("psycopg.pool").disabled = True
controller = PersonsController()
route = PersonsRoute("persons_route", controller)
app.register_blueprint(route)
