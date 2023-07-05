import cv2
from detect import DESIRED_MARKER_ID, calculateCenter, calculateDistanceFromBaseLine, calculateDistanceFromCenter, drawBoundaries, getDetector
import numpy as np
import serial
import json

from uart import sendOverSerial

if __name__ == "__main__":
    # Configure serial port
    # RX = GPIO15, TX = GPIO14
    print("Configuring serial port...")
    ser = serial.Serial('/dev/serial0', 9600, 8, 'N', 1, timeout=1)

    detector = getDetector()
    print("Starting video capture...")
    # Create a video capture object for the default camera
    vcap = cv2.VideoCapture(0)
    width = vcap.get(cv2.CAP_PROP_FRAME_WIDTH)
    halfWidth = width / 2
    height = vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # Vertical base line
    topMiddle = (int(halfWidth), 0)
    bottomMiddle = (int(halfWidth), int(height))

    print("Starting video loop...")
    # Loop over frames from the video stream
    while True:
        # Read a frame from the video stream
        ret, frame = vcap.read()
        
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect AR markers in the grayscale image
        (corners, ids, rejected) = cv2.aruco.detectMarkers(gray, detector[0], parameters=detector[1])

        if ids is not None:
            # flatten the ArUco IDs list
            ids = ids.flatten()
            # search for the desired marker ID
            indices = np.where(ids == DESIRED_MARKER_ID)[0]
            # ensure at least one ArUco marker was found
            if(len(indices) != 0):
                idx = indices[0]
                markerCorner = corners[idx]
                # markerId = ids[idx]

                # extract the marker corners
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                # convert each of the (x, y)-coordinate pairs to integers
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))

                center = calculateCenter(topLeft, bottomRight)

                horizontalDistance = calculateDistanceFromCenter(center, halfWidth)

                depthDistance = calculateDistanceFromBaseLine(topLeft, topRight, bottomRight, bottomLeft)
                depthDistance = abs(depthDistance)

                drawBoundaries(frame, topLeft, topRight, bottomRight, bottomLeft, depthDistance)
                cv2.circle(frame, center, 4, (0, 0, 255), -1)

                # Sending data over UART
                sendOverSerial(ser, {
                    "horizontal": horizontalDistance,
                    "distance": depthDistance
                })
                
        cv2.line(frame, topMiddle, bottomMiddle, (255, 0, 0), 2)
        cv2.imshow('frame', frame)

        # Check for the 'q' key to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all windows
    vcap.release()
    cv2.destroyAllWindows()
    # Close serial port
    ser.close()