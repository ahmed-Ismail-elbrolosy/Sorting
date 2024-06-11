import cv2
import numpy as np

#Specifying upper and lower ranges of color to detect in hsv format
lower = np.array([100, 150, 100])
upper = np.array([140, 255, 255]) # (These ranges will detect Yellow)
lower1 = np.array([170, 100, 100])
upper1 = np.array([180, 255, 255]) # (These ranges will detect Yellow)
#Capturing webcam footage
webcam_video = cv2.VideoCapture(0)

while True:
    success, video = webcam_video.read() # Reading webcam footage

    img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV) # Converting BGR image to HSV format

    mask = cv2.inRange(img, lower, upper) # Masking the image to find our color
    mask1 = cv2.inRange(img, lower1, upper1) # Masking the image to find our color
    mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image
    mask_contours1, hierarchy1 = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Finding position of all contours
    if len(mask_contours) != 0:
        for mask_contour in mask_contours:
            if cv2.contourArea(mask_contour) > 500:
                x, y, w, h = cv2.boundingRect(mask_contour)
                cv2.rectangle(video, (x, y), (x + w, y + h), (255, 0, 0), 3) #drawing rectangle
                cv2.putText(video, "Blue Colour", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (255, 0, 0))

    if len(mask_contours1) != 0:
        for mask_contour1 in mask_contours1:
            if cv2.contourArea(mask_contour1) > 500:
                x, y, w, h = cv2.boundingRect(mask_contour1)
                cv2.rectangle(video, (x, y), (x + w, y + h), (0, 0, 255), 3) #drawing rectangle
                cv2.putText(video, "Red Colour", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (0, 0, 255))



    cv2.imshow("Blue Mask", mask) # Displaying mask image
    cv2.imshow("Red Mask", mask1)  # Displaying
      
    cv2.imshow("frame", video)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv2.destroyAllWindows()