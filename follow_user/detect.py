import cv2
import numpy as np
import time

DESIRED_MARKER_ID = 27
DEBUG = True
KNOWN_LENGTH = 15.2
FOCAL_LENGTH = 780

def getDetector():
    # Define the AR marker dictionary
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    # Define the parameters for the AR marker detector
    parameters =  cv2.aruco.DetectorParameters_create()
    return dictionary, parameters

def drawText(image, text, position, color):
    cv2.putText(
        image,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        color,
        2
    )

def drawBoundaries(image, topLeft, topRight, bottomRight, bottomLeft, distanceInCm):
    cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
    cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
    cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
    cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)

    drawText(image, str(distanceInCm) + ' cm', (topRight[0], topRight[1] - 15), (0, 0, 255))
    

def calculateCenter(topLeft, bottomRight):
    """ Returns the center of the marker
    """
    cX = int((topLeft[0] + bottomRight[0]) / 2.0)
    cY = int((topLeft[1] + bottomRight[1]) / 2.0)

    if(DEBUG):
        print("Center: ", cX, cY)
    
    return (cX, cY)

def calculateDistanceFromCenter(center, halfWidth):
    """ Returns the distance from the center of the screen to the center of the marker
    Positive means the marker is to the left of the center
    """
    (cX, cY) = center
    distanceX = (halfWidth - cX) / halfWidth

    if(DEBUG):
        print("Distance from center: ", distanceX)

    return distanceX

def calculateDistanceFromBaseLine(topLeft, topRight, bottomRight, bottomLeft):
    topWidth = topRight[0] - topLeft[0]
    bottomWidth = bottomRight[0] - bottomLeft[0]
    rightHeight = bottomRight[1] - topRight[1]
    leftHeight = bottomLeft[1] - topLeft[1]

    width = int((topWidth + bottomWidth) / 2)
    height = int((rightHeight + leftHeight) / 2)

    distance = distance_to_camera(width)
    distanceHeight = distance_to_camera(height)

    if(DEBUG):
        # print("Top X size: ", topWidth)
        # print("Bottom X size: ", bottomWidth)
        print("Width: ", width)
        print("Distance: ", distance)
        print("Distance height: ", distanceHeight)

    return round(distanceHeight, 2)

def distance_to_camera(pixelLength, knownLength=KNOWN_LENGTH, focalLength=FOCAL_LENGTH):
    """compute and return the distance from the maker to the camera

    Args:
        pixelWidth (int): Width in pixels of the marker on the image
        knownWidth (int, optional): Width of the real object. Defaults to KNOWN_WIDTH.
        focalLength (int, optional): Focal length of the camera. Defaults to FOCAL_LENGTH.

    Returns:
        int: Distance in cm
    """
    return (focalLength * knownLength) / pixelLength

if __name__ == "__main__":
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
                

        # Display the resulting image
        # frame = cv2.resize(frame, (int(width*2), int(height*2)))
        cv2.line(frame, topMiddle, bottomMiddle, (255, 0, 0), 2)
        cv2.imshow('frame', frame)
        # if(DEBUG):
        #     time.sleep(1)
        # Check for the 'q' key to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all windows
    vcap.release()
    cv2.destroyAllWindows()