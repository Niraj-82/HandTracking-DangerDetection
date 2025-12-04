# ✋ Hand Tracking Danger Detection POC
Real-time computer vision system that tracks a user's hand and triggers a **DANGER** warning if the hand comes too close to a **virtual safety boundary** on the screen.

This project demonstrates **real-time hand tracking**, **virtual boundary interaction**, and **distance-based safety alerts** using only classical computer vision (no MediaPipe / no cloud models).

---

## 🚀 Features

| Feature | Status |
|--------|:-----:|
| Real-time hand tracking via webcam | ✔ |
| Classical CV techniques (HSV mask, contours) | ✔ |
| Virtual safety boundary (rectangle overlay) | ✔ |
| Distance-based classification | SAFE / WARNING / DANGER |
| On-screen visual feedback for each state | ✔ |
| CPU-only fast execution (≥ 8 FPS) | ✔ |

---

## 🎯 System Output States

| State | Condition | Visual Feedback |
|-------|-----------|----------------|
| SAFE | Hand > 120px from boundary | Green ✔ |
| WARNING | Distance: 60–120px | Yellow ⚠ |
| DANGER | Distance ≤ 60px or touching | 🔴 **“DANGER DANGER”** alert |

---

## 🛠 Tech Stack

- **Python**
- **OpenCV**
- **NumPy**

(No MediaPipe, OpenPose, or cloud AI allowed)

---

## 📂 Project Structure

HandTracking-DangerDetection/
│── main.py
│── hand_tracker.py
│── state_logic.py
│── requirements.txt
└── README.md


---

## 🧠 How It Works

1️⃣ Webcam feed is processed in real time  
2️⃣ Skin/colored object segmentation using **HSV thresholding**  
3️⃣ Largest visible hand region detected via contours  
4️⃣ **Centroid of hand** is calculated  
5️⃣ Distance computed between hand and **virtual rectangle**  
6️⃣ State logic classifies proximity  
7️⃣ Alerts and overlays drawn live

> Calculation uses precise geometric distance between a point and a rectangle.

---

## ▶ Usage Instructions

### Install dependencies
```bash
pip install -r requirements.txt
Run the system
bash
Copy code
python main.py
Keyboard Controls
Key	Action
q	Quit
m	Toggle mask debug view
W / A / S / D	Move the virtual boundary

💡 Tips for Better Tracking
✔ Use good lighting
✔ Keep the hand in lower half of frame
✔ Avoid background with skin-like colors
✔ Optionally wear bright colored tape/glove for better mask detection

🧪 Future Enhancements
Add depth estimation for more accurate proximity

Audio alarm in Danger state

Multi-hand support

Better segmentation using adaptive skin models

Web interface using Flask or FastAPI
