import numpy as np
import HandTrackingModule as htm
import cv2
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER


# opens the webcam and displays the video
video_capture = cv2.VideoCapture(0)
hand = htm.handDetector()

devices = AudioUtilities.GetSpeakers()
#interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
#volume = cast(interface, POINTER(IAudioEndpointVolume))
volume = devices.EndpointVolume.QueryInterface(IAudioEndpointVolume)
#volume.SetMasterVolumeLevelScalar(volume_level / 100.0, None)

volRange = volume.GetVolumeRange()
minVol = volRange[0]                  # MINIMUM VOLUME
maxVol = volRange[1]                  # MAX VOLUME
vol = 0                               # CURRENT VOLUME
volBar = 400                          # INITIAL POSITION OF VOLUME BAR
volPer = 0                            # PERCENTAGE OF VOLUME



while True:
    result, video_frame = video_capture.read()
    img = hand.findHands(video_frame)
    lmlist, bbox = hand.findPosition(img)
    print (lmlist)
    if lmlist != ([]):
        length, img, [x1, y1, x2, y2, cx, cy] = hand.Distance(img, 4, 20, draw=True)

        vol = np.interp(length, [50, 300], (minVol, maxVol))
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])

    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255,0,0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    if result is False:
        break

    cv2.imshow("My Face Detection Project", img)
    cv2.waitKey(1)   # waits 1 millisecond to update the display

    k = cv2.waitKey(1)
    if k % 256 == 27:      # ESC key to close the program (in ASCII)
        print ("Escape hit, closing...")
        break

video_capture.release()
cv2.destroyAllWindows()