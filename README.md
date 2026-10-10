# cv2-hand-face-tracking

Small computer vision scripts built with OpenCV and MediaPipe: live face detection and hand-gesture tracking over webcam.

## Scripts

- **FaceRecognition.py** — real-time face detection using a Haar cascade classifier. Draws a bounding box per face, counts faces on screen, and supports a few keyboard controls:
  - `r` / `b` / `g` — change the box color
  - `m` — toggle a drawn-on mustache
  - `space` — save a screenshot
  - `esc` — quit

- **HandTrackingModule.py** — a reusable `handDetector` class wrapping MediaPipe Hands: finds hands in a frame, returns landmark positions, and measures the distance between two landmarks (e.g. thumb and pinky tips).

- **CameraHandControl.py** — an app built on `HandTrackingModule`: tracks the distance between your thumb and pinky and maps it to your system's volume in real time. **Windows only** — it uses `pycaw`/`comtypes` to talk to the Windows Core Audio API, so it won't run on macOS/Linux.

## Setup

```sh
pip install opencv-python mediapipe
```

For `CameraHandControl.py` specifically (Windows only):

```sh
pip install pycaw comtypes
```

### A couple of version gotchas

- **OpenCV 5.x removed `cv2.CascadeClassifier`** from the plain `opencv-python` build (it's needed for `FaceRecognition.py`). Stick to the 4.x line:
  ```sh
  pip install "opencv-python<5"
  ```
- **MediaPipe 1.0+ dropped the legacy `mediapipe.solutions` API** that `HandTrackingModule.py` is built on, with no way back via version pinning on newer Python versions. If `mp.solutions` isn't available in your environment, you'll need an older Python (3.10/3.11) where a pre-1.0 MediaPipe build still ships it, or port the module to the newer MediaPipe Tasks API.
- Don't install `opencv-python` and `opencv-contrib-python` side by side — they write to the same folder and will silently clobber each other. Pick one (`opencv-python<5` covers everything these scripts need).

## Run

```sh
python FaceRecognition.py
python CameraHandControl.py
```
