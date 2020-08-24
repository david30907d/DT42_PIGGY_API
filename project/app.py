"""
entrypoint of falcon
"""
import os

import falcon

from project.database import SESSION
from project.resources import PiggyResource, VideoResource, DashBoardResource
from project.middleware import ConnectionManager

if os.getenv("STAGING"):
    from falcon_cors import CORS

    cors = CORS(allow_all_origins=True, allow_all_headers=True, allow_all_methods=True,)
    app = application = falcon.API(
        middleware=[ConnectionManager(SESSION), cors.middleware]
    )
else:
    app = application = falcon.API(middleware=[ConnectionManager(SESSION)])

app.add_route("/settings", PiggyResource())
app.add_route("/dashboard", DashBoardResource())
app.add_route("/videofeed", VideoResource())
