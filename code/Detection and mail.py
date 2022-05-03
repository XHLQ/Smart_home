#-*-coding:utf-8-*-

import RPi.GPIO as GPIO
import argparse
import datetime
import imutils
import time
import cv2

import threading
import yagmail

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())
shot_idx = 0
# If the video parameter is None, then we read the data from the camera
if args.get("video", None) is None:
    camera = cv2.VideoCapture(0)#Open camera 0 directly to get image

# Otherwise we read a video file
else:
    camera = cv2.VideoCapture(args["video"])




def shijue() :
    shot_idx = 0
   # loop through each frame of the video
    # Initialize the first frame of the video stream
    firstFrame = None
    while True:

       # Read in the camera frame
        (grabbed, frame) = camera.read()
        text = "Stop"
        flat = 0
      # If we can't grab a frame, we've reached the end of the video
        if not grabbed:
            break
        cv2.imshow('frame',frame)
       # Resize the frame, convert to grayscale and apply Gaussian blur to it
        frame = imutils.resize(frame, width=500)
       # Preprocess the frame, first convert the grayscale image, and then perform Gaussian filtering.
        # Blur with Gaussian filtering, the reason for the processing: Each input video will have noise due to natural vibration, lighting changes, or the camera itself. Noise is smoothed to avoid detection during motion and tracking。
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        cv2.imshow('gray', gray)
    # If the first frame is None, initialize it

        if firstFrame is None:
            firstFrame = gray
#If the first frame does not exist at the beginning of detection, then use the grayscale image as the first frame
            continue
        # Calculate the difference between the current frame and the first frame
        # For each frame read from the background, the difference from Beijing is calculated and a difference map is obtained.
        # Also need to apply a threshold to get a black and white image, and dilate the image with the following code to normalize holes and imperfections
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        firstFrame = gray

       # Expand the threshold image to fill the hole, then find the contour on the threshold image
        thresh = cv2.dilate(thresh, None, iterations=2)
        #search contour
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                                      cv2.CHAIN_APPROX_SIMPLE)
       #Opencv4 is used here, cv2.findContours returns 2 parameters, but if opencv3 is used, it will return 3 to parameters, you must ensure that there are enough variables to undertake the return value and can be changed to binary, contours, hierarchy = cv.findContours(thresh , cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        #Return value: contours: a list, each item is a contour, it will not store all the points of the contour, only the points that can describe the contour hierarchy: an ndarray, the number of elements is the same as the number of contours, each contour contours[i ] corresponds to 4 hierarchy elements hierarchy[i][0] ~hierarchy[i][3], which represent the index numbers of the next contour, previous contour, parent contour, and embedded contour respectively. If there is no corresponding item, the value is negative
       
        for c in contours:
            # The outline is too small to ignore, it may be speckle noise

            if cv2.contourArea(c) < 5000:  # Recognition range or accuracy， args["min_area"]
                continue
           # draw the outline
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            # Calculate the bounding box of the contour, draw the box in the current frame
            flat = 1   # Set a label to 1 when there is motion
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Moving"
            # Show sports on screen
            led = True
            if led == True:
                    #LED
                for i in range(30):
                    GPIO.output(18,GPIO.HIGH)
                    time.sleep(0.03)
                    GPIO.output(18,GPIO.LOW)
                    time.sleep(0.03)
                    GPIO.output(18,GPIO.LOW)
                    #Buzzer
                    GPIO.output(11,GPIO.HIGH)
                    time.sleep(0.03)
                    GPIO.output(11,GPIO.LOW)
                    time.sleep(0.03)
                    GPIO.output(11,GPIO.LOW)
                    
        # draw the text and timestamp on the frame
        
        cv2.putText(frame, "Movement State: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # Display the current frame and record whether the user pressed a key

        cv2.imshow("Thresh", thresh)
        cv2.imshow("Frame Delta", frameDelta)
        cv2.imshow("Security Feed", frame)
        #cv2.imwrite("/home/pi/Desktop/detection_email/image.jpg", frame)#Save to a location, here is the Raspberry Pi
        if cv2.waitKey(1) & 0xFF == ord('q'): 
             #cv2.imwrite("E:\cpy\pictures\\pic.jpg", frame1)
            break

    camera.release()
    cv2.destroyAllWindows()


def qqyouxian(num):
    yag = yagmail.SMTP(user="1213105346@qq.com", password="unmhhalpxsswgfid", host="smtp.qq.com")
    
    contents = ["Moving objects have been detected", "/home/pi/Desktop/detection_email/image.jpg"]

    yag.send("yuanshengy@163.com", "Moving objects have been detected", contents)
    yag.close()
    
    time.sleep(5)


def main():
#Designed for multi-threaded parallelism, mail sending and machine vision parts do not conflict

    t_sing = threading.Thread(target=shijue)
    t_dance = threading.Thread(target=qqyouxian, args=(6, ))
    t_sing.start()
    t_dance.start()


if __name__ == '__main__':
    main()
    
          