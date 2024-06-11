#!/usr/bin/python3
#license removed for brevity

import cv2
import numpy as np
import rospy
from std_msgs.msg import String

# ROS initialization
rospy.init_node('publisher', anonymous=True)
pub = rospy.Publisher('Detection', String, queue_size=10)

# Shape detector function
def shape_detector(contour):
    shape = ""
    shape_detected = False
    area = cv2.contourArea(contour)
    
    # Filter out very small contours
    if area < 1000:  # Adjust this threshold as needed
        return "no shape"
    
    # Approximate the shape
    epsilon = 0.04 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    
    # Draw contours
    cv2.drawContours(frame, [contour], 0, (0, 0, 255), 5)
    
    # Finding center point of shape
    M = cv2.moments(contour)
    if M['m00'] != 0.0 and not shape_detected:  # Check if a shape has not been detected yet
        x = int(M['m10'] / M['m00'])
        y = int(M['m01'] / M['m00'])

    # Label the shape
     # Label the shape
    if len(approx) == 3: 
        cv2.putText(frame, 'Triangle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        shape = "Triangle"
        shape_detected = True  # Set the flag to True
    elif len(approx) == 4:
        # Check if the contour is approximately a square
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h
        if 0.95 <= aspect_ratio <= 1.05:
            cv2.putText(frame, 'Square', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            shape = "Square"
        else:
            cv2.putText(frame, 'Quadrilateral', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            shape = "Quadrilateral"
        shape_detected = True  # Set the flag to True
    elif len(approx) == 5: 
        cv2.putText(frame, 'Pentagon', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        shape = "Pentagon"
        shape_detected = True  # Set the flag to True
    elif len(approx) == 6: 
        cv2.putText(frame, 'Hexagon', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        shape = "Hexagon"
        shape_detected = True  # Set the flag to True
    else: 
        cv2.putText(frame, 'Circle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        shape = "Circle"
        shape_detected = True  # Set the flag to True

    return shape

# Color detector
def color_detector(pixel_center):
    hue_value = pixel_center[0]
    sat_value = pixel_center[1]
    val_value = pixel_center[2]
    color = ""

    if sat_value < 30 and val_value > 220:
        color = "WHITE"
    elif val_value < 30:
        color = "BLACK"
    elif hue_value < 5:
        color = "RED"
    elif hue_value < 22:
        color = "ORANGE"
    elif hue_value < 33:
        color = "YELLOW"
    elif hue_value < 78:
        color = "GREEN"
    elif hue_value < 131:
        color = "BLUE"
    elif hue_value < 167:
        color = "VIOLET"
    else:
        color = "RED"

    return color

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width, _ = frame.shape

    cx = int(width / 2)
    cy = int(height / 2)
    radius = 350

    # Pick pixel value
    pixel_center = hsv_frame[cy, cx]

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    shape=""
    # Loop through contours
    for contour in contours:
        if cv2.contourArea(contour) > 250:
            # Check if contour center is within the defined circle
            M = cv2.moments(contour)
            if M['m00'] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                if (cX - cx)**2 + (cY - cy)**2 <= radius**2:
                    shape = shape_detector(contour)
                    cv2.putText(frame, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    pixel_center_bgr = frame[cy, cx]
    b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])
    color = color_detector(pixel_center)
    cv2.putText(frame, color, (10, 50), 0, 1, (b, g, r), 2)
    cv2.circle(frame, (cx, cy), radius, (b, g, r), 2)


    if color in ["BLUE", "GREEN"] and shape in ["Square", "quadrilateral"] :
        pub.publish("Blue color detected!")
        print(color, shape)

    elif color in ["RED", "ORANGE","YELLOW","WHITE"] and shape in ["Square", "Quadrilateral", "Circle"] :
        pub.publish("Red color detected!")
        print(color, shape)
    
    cv2.imshow("frame", frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
