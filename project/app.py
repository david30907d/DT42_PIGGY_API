"""
entrypoint of falcon
"""
import falcon

from project.database import SESSION
from project.resources import PiggyResource, DashBoardResource
from project.middleware import ConnectionManager

app = application = falcon.API(middleware=[ConnectionManager(SESSION)])

app.add_route("/settings", PiggyResource())
app.add_route("/dashboard", DashBoardResource())
