"""
entrypoint of falcon
"""
import os

import falcon

from project.database import SESSION
from project.resources import (
    AuthResource,
    PiggyResource,
    VideoResource,
    DashBoardResource,
)
from project.middleware import ConnectionManager

app = application = falcon.API(middleware=[ConnectionManager(SESSION)])

app.add_route("/settings", PiggyResource())
app.add_route("/dashboard", DashBoardResource())
app.add_route("/videofeed", VideoResource())
app.add_route("/auth", AuthResource())
