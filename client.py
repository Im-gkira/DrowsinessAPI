import base64
from imutils.video import VideoStream
import requests
import time
import cv2

print("[INFO] starting video stream thread...")
cap = cv2.VideoCapture(0)


# loop over frames from the video stream
while True:
    # Capture a frame from the video stream
    ret, frame = cap.read()

    # Encode the frame as a JPEG image
    _, encoded_frame = cv2.imencode(".jpg", frame)

    # Convert the encoded frame to base64
    base64_frame = base64.b64encode(encoded_frame).decode('utf-8')

    # Set up the payload with the base64 frame
    payload = {"captured": base64_frame}

    # Send the frame to the server
    response = requests.post("http://localhost:5000/api/drowsiness_check", json=payload)
    print(response.text)
    # Check the response status code
    if response.status_code != 200:
        print("Error sending frame")
        break

cap.release()
cv2.destroyAllWindows()
