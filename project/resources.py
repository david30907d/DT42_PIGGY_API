"""
some comment
"""
import json
import time
from pathlib import Path
from datetime import datetime
from imutils.video import VideoStream
import cv2
import falcon

from config.config import LOCATION


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


class VideoResource:
    """
    Resource of video stream
    """

    def on_get(self, _, resp):
        labeled_frame = self._get_frame(VideoStream(src=0, usePiCamera=True).start())
        resp.content_type = "multipart/x-mixed-replace; boundary=frame"
        resp.stream = labeled_frame

    def _get_frame(self, camera, frame_count_threshold=50000):
        # wait for camera resource to be ready
        time.sleep(2)

        frame_count = 0
        while True:
            if frame_count % frame_count_threshold == 0:
                image = camera.read()
                _, jpeg = cv2.imencode(".jpg", image)
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
                )
            frame_count += 1
