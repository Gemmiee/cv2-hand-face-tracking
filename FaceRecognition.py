import cv2
from datetime import datetime

# opens the webcam and displays the video
video_capture = cv2.VideoCapture(0)
face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

box_color = (0, 255, 0)
mustache_on = False

def detect_bounding_box(vid):
    # converts the image to grayscale for better face detection
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40,40))
    for (x, y, w, h) in faces:
        cv2.rectangle(vid, (x,y), (x+w, y+h), box_color, 4)    # x+w kai y+h einai oi synetagmenes gia to katw deksia kommati tou
        if mustache_on:
            mustache_y = y+ int(h*0.65)
            cv2.rectangle(vid, (x+ int(w * 0.25), mustache_y),
                          (x+ int(w * 0.75), mustache_y + int(h * 0.1)), (0,0,0), -1)
    #print(f'Found {len(faces)} faces!')                          # tetragwnou pou tha zwgrafistei
    return faces


while True:
    result, video_frame = video_capture.read()
    if result is False:
        break

    faces = detect_bounding_box(video_frame)

    # displays the number of faces on the screen
    face_count = len(faces)
    cv2.putText(video_frame, f'Faces: {face_count}', (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("My Face Detection Project", video_frame)
    cv2.waitKey(1)   # waits 1 millisecond to update the display

    k = cv2.waitKey(1)
    if k % 256 == 27:      # ESC key to close the program (in ASCII)
        print ("Escape hit, closing...")
        break
    elif k % 256 == ord('r'):   # red, by pressing R on keyboard
        box_color = (0,0,255)
        print("Turned into red")
    elif k % 256 == ord('b'):   # blue, by pressing B on keyboard
        box_color = (255, 0, 0)
        print ("Turned into blue")
    elif k % 256 == ord('g'):   # green, by pressing G on keyboard
        box_color = (0, 255, 0)
        print ("Turned into green")
    elif k % 256 == 32:         # spacebar to save a screenshot
        now = datetime.now()
        img_name = "frame_at_time_" + str(now.hour) + "." + str(now.minute) + "." + str(now.second) + ".png"
        cv2.imwrite(img_name, video_frame)
        print(f'Picture saved as {img_name}')
    elif k % 256 == ord('m'):    # toggles mustache
        mustache_on = not mustache_on
        print("Mustache mode: "+ ("ON" if mustache_on else "OFF"))

video_capture.release()
cv2.destroyAllWindows()