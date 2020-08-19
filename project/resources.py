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
        destination = Path(req.media["filepath"])
        if not destination.exists():
            destination.mkdir(parents=True, exist_ok=True)
        with open(destination.joinpath("settings.json"), "w") as file:
            json.dump(req.media["payload"], file)
        resp.status = falcon.HTTP_201
        resp.media = {"status": "success"}


class DashBoardResource:
    """
    A resource for dashboard
    """

    def on_get(self, req, resp) -> None:
        """
        Get records from DB
        """
        result = []
        keys = ("CHANNEL", "TIMESTAMP", "ANNOTATIONS")
        for value in req.context["sess"].execute(
            "SELECT CHANNEL, TIMESTAMP, ANNOTATIONS FROM ODS_FARM_ID_TIMESTAMP;"
        ):
            payload = dict(zip(keys, value))
            payload["TIMESTAMP"] = str(payload["TIMESTAMP"])
            payload["ANNOTATIONS"] = [
                annotation["label"] for annotation in json.loads(payload["ANNOTATIONS"])
            ]
            result.append(payload)
        resp.media = result
