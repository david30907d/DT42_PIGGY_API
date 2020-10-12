"""
entrypoint of falcon
"""
import falcon

from project.database import SESSION
from project.resources import (
    AuthResource,
    PiggyResource,
    VideoResource,
    DashBoardResource,
)
from project.middleware import ConnectionManager

if os.getenv("LOCATION") in ("dev", "pytest"):
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
app.add_route("/auth", AuthResource())
