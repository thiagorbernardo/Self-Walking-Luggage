import cv2
import numpy as np

# Define the AR marker dictionary
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
# Define the parameters for the AR marker detector
parameters =  cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)

DESIRED_MARKER_ID = 27

# Create a video capture object for the default camera
vcap = cv2.VideoCapture(0)

# Loop over frames from the video stream
while True:
    # Read a frame from the video stream
    ret, frame = vcap.read()

    width = vcap.get(cv2.CAP_PROP_FRAME_WIDTH)
    halfWidth = width / 2
    height = vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # Vertical base line
    topMiddle = (int(halfWidth), 0)
    bottomMiddle = (int(halfWidth), int(height))
    cv2.line(frame, topMiddle, bottomMiddle, (255, 0, 0), 3)
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect AR markers in the grayscale image
    (corners, ids, rejected) = detector.detectMarkers(gray)

    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

    if ids is not None:
        # flatten the ArUco IDs list
        ids = ids.flatten()

        # loop over the detected ArUCo corners
        for (markerCorner, markerID) in zip(corners, ids):
            if(markerID != DESIRED_MARKER_ID):
                continue
            # extract the marker corners
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            # convert each of the (x, y)-coordinate pairs to integers
            # topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            # bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))

            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)

            xDistanceFromCenter = (halfWidth - cX) / halfWidth
            # positive means the marker is to the left of the center

            print(xDistanceFromCenter)
            # if xDistanceFromCenter > 0:
            #     print("Turn left")
            # elif xDistanceFromCenter < 0:
            #     print("Turn right")
            # else:
            #     print("Go straight")
            # print("Center: ", cX, cY)
            cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
    
    # Display the resulting image
    cv2.imshow('frame', frame)
    
    # Check for the 'q' key to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
vcap.release()
cv2.destroyAllWindows()