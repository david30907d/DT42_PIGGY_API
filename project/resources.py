"""
some comment
"""
import json
import time
from pathlib import Path

import cv2
import falcon
import requests
from marshmallow import fields
from webargs.falconparser import use_args

from dt42lab.core import tools
from config.config import PIPELINE, LINE_TOKEN
from project.utils import line_notify_message

SESS = requests.session()


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

    argmap = {"cameraId": fields.Str()}

    @use_args(argmap, location="query")
    def on_get(self, _, resp, args):
        line_notify_message(SESS, LINE_TOKEN, "from falcon XDD")
        camera_src = self._get_camera_src(args)
        labeled_frame = self._get_frame(cv2.VideoCapture(camera_src))
        resp.content_type = "multipart/x-mixed-replace; boundary=frame"
        resp.stream = labeled_frame

    @staticmethod
    def _get_camera_src(args):
        settings_json = Path(args["cameraId"]) / "settings.json"
        camera_src = json.loads(settings_json.read_text())["Source"]
        if camera_src.isnumeric():
            camera_src = int(camera_src)
        return camera_src

    @staticmethod
    def _get_frame(camera, frame_count_threshold=5000):
        # wait for camera resource to be ready
        time.sleep(2)
        ext_meta = tools.parse_json("config/meta.json", "utf-8")
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        fps = camera.get(cv2.CAP_PROP_FPS)
        frame_count = 0
        print(f"FPS: {fps/frame_count_threshold}")
        while True:
            if frame_count % frame_count_threshold == 0:
                _, frame = camera.read()
                PIPELINE.run(
                    frame, external_meta=ext_meta, benchmark=False,
                )
                _, jpeg = cv2.imencode(".jpg", PIPELINE.output[0])
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
                )
            frame_count += 1
