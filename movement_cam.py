import cv2
import imutils
import time
import threading
change_frame = True
die = False
class sleeper(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global change_frame
        global die

    def run(self):
        while True:
            time.sleep(10)
            #print("10s passed, new frame")
            global change_frame
            change_frame = True
            
            if die:
                break;

def main():        
    print(cv2.__version__)
    global die
    cap = cv2.VideoCapture(0)
    comp_frame = None #comparison frame (for background)
    t = sleeper()
    t.start()

    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    comp_frame = gray

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        global change_frame
        if change_frame == True:
            comp_frame = gray
            change_frame = False
            
        #will be a diff if movement
        frameDelta = cv2.absdiff(comp_frame, gray)
        thresh = cv2.threshold(frameDelta, 80, 255, cv2.THRESH_BINARY)[1]

        thresh = cv2.dilate(thresh, None, iterations=2) #make diff bright

        #find contours and grab them
        countours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        countours = imutils.grab_contours(countours)

        for cnt in countours:
            # if the contour is too small and deemed to be noise, ignore it
            if cv2.contourArea(cnt) < 200:
                continue
            # compute the bounding box for the contour, draw it on the frame,

            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the resulting frames
        cv2.imshow('frame',frame)
        cv2.imshow("Threshholds", thresh)
        #cv2.imshow("Frame Delta", frameDelta)
        #press c to break loop
        if cv2.waitKey(1) & 0xFF == ord('c'):
            die = True
            break


    # When everything done, release the capture and destroy windows
    cap.release()
    cv2.destroyAllWindows()
    t.join()
    print("Shutdown successful")

if __name__ == '__main__':
    main()
