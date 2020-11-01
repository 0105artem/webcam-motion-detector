# motion_detector.py - detects any moving objects using your web camera and stores 
# and visualizes the times when the object entered and exited the video frame.
# Made with OpenCV, Bokeh and pandas libraries.

import cv2, time, pandas
from datetime import datetime

first_frame = None
status_list = [None, None]
times = []
df = pandas.DataFrame(columns=["Start", "Endtime"])

video = cv2.VideoCapture(0)

while True:
    check, frame = video.read()

    # If there's any moving object status = 1 otherwise 0
    status = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Make it blured to get rid of the noices.
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # First frame of the video which stands for a background.
    if first_frame is None:
        first_frame = gray
        continue
    
    # Compare first frame (background) with the current frame.
    delta_frame = cv2.absdiff(first_frame, gray)

    # thresh_frame stands for threshold between first_frame and current 
    # frame. If the color difference of the first frame and the current 
    # frame is more than 25, we'll classify that as white, otherwise as 
    # black. So we'll say there's probably motioning in those pixels. 
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    
    # Making threshold frame more smooth and clear.
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)
    
    # Finding contours of moving objects.
    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get rid of extra contours.
    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            continue
        status = 1
         
        # Parameters that defines the rectangle of the contour.
        (x, y, w, h) = cv2.boundingRect(contour)

        # Draw rectangle to frame
        cv2.rectangle(frame, (x, y), (x+w, y+h), (49, 200, 100), 3)

    status_list.append(status)
    
    # We need to compare only 2 last elemets of status_list, it'll keep memory clean
    status_list = status_list[-2:]

    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now()) 
    
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)
    key = cv2.waitKey(1)

    if key == ord('q'):
        # In case if status == 1 when the loop stops working 
        # we need to add endtime for the last moving object.
        if status == 1:
            times.append(datetime.now())
        break

for i in range(0, len(times), 2):
    df = df.append({"Start": times[i], "Endtime": times[i+1]}, ignore_index = True)

df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows


