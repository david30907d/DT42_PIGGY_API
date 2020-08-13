"""
entrypoint of falcon
"""
import falcon

from project.database import SESSION
from project.resources import PiggyResource
from project.middleware import ConnectionManager

app = application = falcon.API(middleware=[ConnectionManager(SESSION)])

app.add_route("/settings", PiggyResource())
