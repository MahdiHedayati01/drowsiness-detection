# Drowsiness Detection Using MediaPipe and OpenCV

## Overview
This project implements a real-time drowsiness detection system using OpenCV and MediaPipe's FaceMesh module. It can be applied in scenarios like monitoring driver alertness during long journeys or ensuring attentiveness in security and surveillance roles. The system monitors a user's eye aspect ratio (EAR) to detect signs of drowsiness and triggers an alert when the eyes remain closed for a specified duration.

## Features
- Real-time detection of facial landmarks using MediaPipe FaceMesh.
- Calculation of Eye Aspect Ratio (EAR) to monitor eye closure.
- Drowsiness detection with customizable thresholds.
- Visual feedback on the detected EAR and drowsiness status.
- Audio alert triggered during prolonged eye closure.

## Requirements

### Software
- Python 3.7 or higher
- OpenCV
- MediaPipe
- NumPy

### Hardware
- A computer with a webcam

## Installation

1. 🛠️ Clone the repository:
    ```bash
    git clone https://github.com/<your-username>/drowsiness-detection.git
    cd drowsiness-detection
    ```

2. 📦 Install required Python packages:
    ```bash
    pip install opencv-python mediapipe numpy
    ```

3. (Optional) 🎵 Ensure your system supports the audio alert command `play` by installing the `sox` package. On Ubuntu, you can install it using:
    ```bash
    sudo apt-get install sox
    ```

## Usage

1. ▶️ Run the script:
    ```bash
    python drowsiness_detection.py
    ```

2. The webcam will start, and the system will begin analyzing facial landmarks in real-time.

3. If drowsiness is detected (both eyes remain closed for the defined `WAIT_TIME` seconds), a visual alert will appear on the screen, and an audio alert will play.

4. Press `q` to quit the application.

## Configuration

- **EAR_THRESH**: Adjust this value to set the threshold for detecting closed eyes. Default is `0.25`.
- **WAIT_TIME**: Set the time (in seconds) for which eyes must remain closed to trigger the alert. Default is `2` seconds.
- **duration**: Define the duration of the audio alert in seconds. Default is `0.3` seconds.
- **freq**: Set the frequency of the audio alert tone in Hz. Default is `580` Hz.

## Code Explanation

### Eye Aspect Ratio (EAR)
EAR is calculated using specific facial landmarks for the eyes. It is an effective metric for detecting drowsiness because it measures the proportion of eye openness, providing a reliable indicator of whether the eyes are closing or remaining shut.
```math
EAR = (|p2-p6| + |p3-p5|) / (2 * |p1-p4|)
```
Where `p1` to `p6` are the coordinates of specific eye landmarks.

### Workflow
1. Capture video frames from the webcam.
2. Use MediaPipe FaceMesh to detect facial landmarks.
3. Calculate EAR for both eyes.
4. Monitor EAR and check if it is below the threshold.
5. If eyes remain closed for `WAIT_TIME` seconds, trigger an alert.

## Sample Output
- EAR value is displayed in real-time on the video feed.
- Visual feedback highlights eye landmarks and alerts if drowsiness is detected.

## Limitations
- Performance may vary in poor lighting conditions.
- May not work accurately for individuals wearing glasses or with unusual eye shapes.

## Future Improvements
- Adaptive thresholding based on individual eye characteristics.
- Integration with additional sensors for enhanced accuracy.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- [MediaPipe](https://mediapipe.dev) for providing a powerful FaceMesh solution.
- [OpenCV](https://opencv.org) for real-time computer vision capabilities.

---

Feel free to contribute and enhance this project! Submit issues or pull requests on the GitHub repository.

