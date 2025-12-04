# ✋ Hand Tracking Danger Detection – Real-Time Safety POC

This project demonstrates a **computer vision–based safety system** that tracks a user’s hand in real time using a standard webcam and triggers alerts when the hand approaches a **virtual safety boundary** on the screen.

Built entirely with **classical Computer Vision** (no MediaPipe, no OpenPose, no cloud AI).

---

## 🚀 Key Features

- 🖐 Real-time hand tracking with OpenCV
- 🔳 Virtual object represented as a boundary rectangle
- 📏 Dynamic distance-based state logic:
  - SAFE → Hand far from danger zone  
  - WARNING → Hand approaching zone  
  - DANGER → Hand touches/enters the boundary
- ⚠️ Clear on-screen alerts including **“DANGER DANGER”**
- ⚡ Runs CPU-only with ≥ 8 FPS performance
- 🖥 Easy to run on any laptop webcam

---

## 🎯 System Behavior

| State | Distance Condition | On-Screen Indication |
|-------|------------------|---------------------|
| 🟢 SAFE | `d > 120 px` | Green text |
| 🟡 WARNING | `60 px < d ≤ 120 px` | Yellow text |
| 🔴 DANGER | `d ≤ 60 px or touching` | **“DANGER DANGER”** alert in red |

Distance = pixel distance between **hand centroid** and **virtual rectangle** edge.

---

## 🛠 Tech Stack

- Python 3.x
- OpenCV (cv2)
- NumPy

---

## 📂 Project Structure

HandTracking-DangerDetection/
│── main.py # Main program with video stream + logic + overlays
│── hand_tracker.py # Hand segmentation + contour detection
│── state_logic.py # Distance + SAFE/WARNING/DANGER classification
│── requirements.txt # Dependencies
└── README.md # Documentation

yaml
Copy code

---

## ▶ Setup & Usage

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
2️⃣ Run the Application
bash
Copy code
python main.py
3️⃣ Keyboard Controls
Key	Action
q	Quit application
m	Toggle mask debug view
W / A / S / D	Move the virtual boundary rectangle

✋ Tips for Better Hand Detection
Use good lighting (front-facing brightness)

Keep hand in the lower half of the frame

Avoid backgrounds with skin-like colors

Optionally place colored tape or paper on hand for higher accuracy

Adjust HSV range for your environment if needed

Press m to see the segmentation mask and tune HSV if required.

🧠 How It Works (Brief)
1️⃣ Capture frame from webcam
2️⃣ Convert frame → HSV color space
3️⃣ Threshold HSV range to isolate hand region
4️⃣ Find largest contour = hand segment
5️⃣ Calculate centroid of contour
6️⃣ Compute minimum distance to rectangle
7️⃣ Display state & overlay alert text in real time

No AI pose-estimation — designed to meet classical CV requirement.

🧩 Future Enhancements (Optional)
🤖 ML-based skin detection for improved accuracy

🔊 Sound alerts in DANGER state

🌐 Optional Flask / FastAPI web streaming dashboard

📊 Log event history & distance trends

🧍 Multi-hand support
