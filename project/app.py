"""
entrypoint of falcon
"""
import falcon

from project.database import SESSION
from project.resources import PiggyResource, DashBoardResource
from project.middleware import ConnectionManager
from falcon_cors import CORS    
cors = CORS(
    allow_origins_list=['http://localhost:3000'],
    allow_all_headers=True,
    allow_all_methods=True,
)

app = application = falcon.API(middleware=[ConnectionManager(SESSION), cors.middleware])

app.add_route("/settings", PiggyResource())
app.add_route("/dashboard", DashBoardResource())
