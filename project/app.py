"""
entrypoint of falcon
"""
import falcon

from project.database import SESSION
from project.resources import PiggyResource, DashBoardResource
from project.middleware import ConnectionManager
import os
if os.getenv('STAGING'):
    from falcon_cors import CORS    
    cors = CORS(
        allow_origins_list=['http://localhost:3000', 'http://localhost:8000'],
        allow_all_headers=True,
        allow_all_methods=True,
    )
    app = application = falcon.API(middleware=[ConnectionManager(SESSION), cors.middleware])
else:
    app = application = falcon.API(middleware=[ConnectionManager(SESSION)])

app.add_route("/settings", PiggyResource())
app.add_route("/dashboard", DashBoardResource())
