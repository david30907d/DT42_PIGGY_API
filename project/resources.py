"""
some comment
"""
import json
import time
from uuid import uuid4
from pathlib import Path
from datetime import datetime, timedelta

import cv2
import jwt
import falcon
import requests
from marshmallow import fields
from webargs.falconparser import use_args

from dt42lab.core import tools
from config.config import (
    SECRET,
    LOCATION,
    PIPELINE,
    LINE_TOKEN,
    GMAIL_TOKEN,
    KAFKA_CONFIG,
    EMAIL_OF_SENDER,
    EMAIL_OF_RECEIVER,
)
from project.utils import send_gmail, notify_line_message

SESS = requests.session()


class AuthResource:
    """
    A resource for authorization and authentication
    """

    @staticmethod
    def on_get(req, resp, resource={}, params={}) -> None:
        """
        For health check probes.
        """
        resp.media = {"authorized": False}
        authorization_header = req.get_header("Authorization")
        if not authorization_header:
            return
        bearer_token = authorization_header.replace("Bearer ", "")
        try:
            jwt.decode(
                bearer_token.encode("utf-8"),
                SECRET,
                audience="dt42_piggy_api",
                issuer="dt42.com",
            )
            resp.media["authorized"] = True
        except jwt.exceptions.InvalidSignatureError:
            pass
        except jwt.exceptions.ExpiredSignatureError:
            pass
        except jwt.exceptions.InvalidIssuerError:
            pass

    def on_post(self, req, resp) -> None:
        """
        save user's payload into settings.json according to privided path
        """
        email = req.media["email"]
        payload = {
            "iss": "dt42.com",
            "sub": email,
            "aud": "dt42_piggy_api",
            "exp": datetime.utcnow() + timedelta(days=7),
            "nbf": datetime.utcnow(),
            "iat": datetime.utcnow(),
            "jti": str(uuid4()),
        }
        # validate email and password
        # some code here

        bearer_token = jwt.encode(payload, SECRET, algorithm="HS256")
        resp.status = falcon.HTTP_201
        resp.media = {"access_token": bearer_token.decode("utf-8"), "token_type": "JWT"}


@falcon.before(AuthResource.on_get)
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


@falcon.before(AuthResource.on_get)
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
                annotation["label"] for annotation in payload["ANNOTATIONS"]
            ]
            result.append(payload)
        resp.media = result


@falcon.before(AuthResource.on_get)
class VideoResource:
    """
    Resource of video stream
    """

    argmap = {"cameraId": fields.Str()}

    @use_args(argmap, location="query")
    def on_get(self, _, resp, args):
        notify_line_message(SESS, LINE_TOKEN, "from falcon XDD")
        send_gmail("TITLE", EMAIL_OF_SENDER, EMAIL_OF_RECEIVER, "CONTENT", GMAIL_TOKEN)
        camera_src = self._get_camera_src(args)
        labeled_image_bytes = self._get_image_bytes(
            cv2.VideoCapture(camera_src), camera_id=args["cameraId"]
        )
        resp.content_type = "multipart/x-mixed-replace; boundary=frame"
        resp.stream = labeled_image_bytes

    @staticmethod
    def _get_camera_src(args):
        settings_json = Path(args["cameraId"]) / "settings.json"
        camera_src = json.loads(settings_json.read_text())["Source"]
        if camera_src.isnumeric():
            camera_src = int(camera_src)
        return camera_src

    @classmethod
    def _get_image_bytes(cls, camera, camera_id, frame_count_threshold=5000):
        frame_count = 0
        fps = cls._get_fps(camera, frame_count_threshold)
        print(f"FPS: {fps}")

        # setup cv2 and meta for inference pipeline
        ext_meta = tools.parse_json("config/meta.json", "utf-8")
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        # wait for camera resource to be ready
        time.sleep(2)

        while True:
            if frame_count % frame_count_threshold == 0:
                frame = cls._get_frame_from_camera(camera)
                jpeg = cls._inference(frame, ext_meta)
                cls._publish_result_2_kafka(camera_id)

                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
                )
            frame_count += 1

    @staticmethod
    def _get_fps(camera, frame_count_threshold) -> float:
        fps = camera.get(cv2.CAP_PROP_FPS)
        return fps / frame_count_threshold

    @staticmethod
    def _get_frame_from_camera(camera):
        if LOCATION == "dev":
            return cv2.imread("fixtures/demo.jpg")
        _, frame = camera.read()
        return frame

    @staticmethod
    def _inference(frame, ext_meta):
        # PIPELINE.run(
        #     frame, external_meta=ext_meta, benchmark=False,
        # )
        # print(PIPELINE.output)
        _, jpeg = cv2.imencode(".jpg", frame)
        return jpeg

    @staticmethod
    def _publish_result_2_kafka(camera_id):
        KAFKA_CONFIG["producer"].send(
            "camera", key=camera_id.encode("utf-8"), value={"333": "$443543"}
        )
