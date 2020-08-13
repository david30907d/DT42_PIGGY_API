"""
some comment
"""
import json
from pathlib import Path

import falcon


class PiggyResource:
    """
    A resource for SMARTAGRI INTEGRATION SERVICE CO., LTD.
    """

    def on_get(self, _, resp) -> None:
        """
        For health check probes.
        """
        resp.body = "ok"

    def on_post(self, req, resp) -> None:
        """
        save user's payload into settings.json according to privided path
        """
        with open(Path(req.media["filepath"]).joinpath("settings.json"), "w") as file:
            json.dump(req.media["payload"], file)
        resp.status = falcon.HTTP_201
