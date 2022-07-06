from gpiozero import Button
import os
import time
import picamera
import datetime
import subprocess
import cv2

button = Button(17)
button2 = Button(22)
button3 = Button(23)
button4 = Button(27)
stillCount=0
startB = 0
stopB = False
#test

# getthetime = time.strftime("%Y%m%d-%H%M%S")
# #Create the folder with the full path
# mydir = "/home/pi/micro/"+getthetime
# os.makedirs(mydir)
img = cv2.imread("UI/script1.png")
screen_res = 1280, 680
scale_width = screen_res[0] / img.shape[1]
scale_height = screen_res[1] / img.shape[0]
scale = min(scale_width, scale_height)
#resized window width and height
window_width = int(img.shape[1] * scale)
window_height = int(img.shape[0] * scale)
#cv2.WINDOW_NORMAL makes the output window resizealbe
cv2.namedWindow('Resized Window', cv2.WINDOW_NORMAL)
#resize the window according to the screen resolution
cv2.resizeWindow('Resized Window', window_width, window_height)


# Called when button is briefly tapped.  Creates Prievew
def preview():
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.start_preview()
        time.sleep(8)
        camera.stop_preview()
        camera.close()


 # Called when button is briefly tapped.  Gathers a micro photo
def gather():
    with picamera.PiCamera() as camera:
        camera.resolution = (4056, 3040)
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        camera.capture(str(timestamp)+'.jpg')


def videoF(input_file_path):
    with picamera.PiCamera() as camera:
        camera.resolution = (1920, 1080)
        camera.framerate = 10
        camera.start_recording(os.path.join(input_file_path, str(timestamp)+'.h264'))
        camera.start_preview()
        camera.wait_recording(40)
        camera.stop_recording()
        camera.stop_preview()
        print('long video Starting')  
# 	global startB
# 	global getthetime
#   # if startB==1:
#     # camera.start_recording(str(getthetime)+'.h264')
#   if startB==2:
# 			camera.stop_recording()
# 			stopB=True
def alt():
    with picamera.PiCamera() as camera:
        camera.resolution = (3280, 2464)
        camera.framerate = 5
        camera.start_recording(str(timestamp)+'.h264')
        camera.start_preview()
        camera.wait_recording(20)
        camera.stop_recording()
        camera.stop_preview()

# def returnToMenu(exit_code=0):

#     # CHECK THIS WORKS!

#     camera.close()
#     cv2.destroyAllWindows()
#     return

def gather_input(input_file_path):
    while True:
        cv2.imshow('Resized Window', img)
        # with picamera.PiCamera() as camera:
        #   camera.resolution = (1280, 720)
        #   camera.framerate = 25
        now = datetime.datetime.now()
        timestamp = now.strftime("%y%m%d%H%M%S")
        if button.is_pressed:
            preview()
            print("preview")
        # else:
        #   print("Button is not pressed")
        if button2.is_pressed:
            gather()
            print("photo taken ")
        # else:
        # print("Button is not pressed")
        if button3.is_pressed:
            videoF(input_file_path)

        if button4.is_pressed: # check this works!
            # returnToMenu()
            # alt() 
            break
        if cv2.waitKey(1) == 27: # escape key exits
            break 

    camera.close()
    cv2.destroyAllWindows()
    return