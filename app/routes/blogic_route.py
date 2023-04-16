import base64

import imutils
from flask_smorest import Blueprint, abort
from flask import jsonify
from flask.views import MethodView
from app import Frame, Response
import cv2
import numpy as np
import argparse
import dlib
from threading import Thread
from scipy.spatial import distance as dist
from imutils import face_utils
import time

bp = Blueprint('bLogic', __name__, url_prefix="/api", description="Drowsiness API")


def eye_aspect_ratio(eye):
    # diff between vertical points
    v1 = dist.euclidean(eye[1], eye[5])
    v2 = dist.euclidean(eye[2], eye[4])

    # diff between horizontal points
    h1 = dist.euclidean(eye[0], eye[3])

    ear = (v1 + v2) / (2.0 * h1)

    return ear


@bp.route("/drowsiness_check")
class DrowsinessCheck(MethodView):
    @bp.response(200, Response)
    @bp.arguments(Frame)
    def post(self, f_data):
        base64_frame = f_data["captured"]

        # Decode the base64 frame to bytes
        frame_bytes = base64.b64decode(base64_frame.encode('utf-8'))
        nparr = np.frombuffer(frame_bytes, np.uint8)

        # Decode the numpy array as an image
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor("D:\Project Based Learning\Flask\drowsiness\static\shape_predictor_68_face_landmarks.dat")

        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        rects = detector(gray, 0)

        EYE_AR_THRESH = 0.2
        EYE_AR_CONSEC_FRAMES = 10
        COUNTER = 0
        WARNING = False
        try:
            for rect in rects:
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                left_eye = shape[lStart:lEnd]
                right_eye = shape[rStart:rEnd]

                left_ear = eye_aspect_ratio(left_eye)
                right_ear = eye_aspect_ratio(right_eye)

                average_ear = (left_ear + right_ear) / 2.0

                if average_ear < EYE_AR_THRESH:
                    COUNTER += 1

                    if COUNTER >= EYE_AR_CONSEC_FRAMES:
                        if not WARNING:
                            WARNING = True
                else:
                    COUNTER = 0
                    WARNING = False
                print(WARNING)
                return {"ear": average_ear, "status": WARNING}
        except Exception as e:
            pass
        return {"ear": -1, "status": WARNING}
