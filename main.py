"""
main.py

Entry point for the hand-to-virtual-boundary interaction POC.

- Opens webcam (cv2.VideoCapture(0))
- Uses HandTracker to find hand centroid
- Computes distance to a fixed central rectangle
- Classifies state into SAFE/WARNING/DANGER using state_logic
- Draws overlays and shows real-time annotated feed
- Exits gracefully on 'q'

Controls:
- 'q' : quit
- 'm' : toggle mask debug window
- WASD: move the virtual rectangle (W=up, S=down, A=left, D=right)
"""

import cv2
import time
from hand_tracker import HandTracker
from state_logic import distance_point_to_rect, classify_state


def clamp(val, vmin, vmax):
    return max(vmin, min(vmax, val))


def main():
    # Target frame size
    FRAME_W, FRAME_H = 640, 480

    # Virtual rectangle coordinates (center region)
    rect_x1, rect_y1 = 220, 140
    rect_x2, rect_y2 = 420, 340

    # Initialize video capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Could not open webcam. Make sure a webcam is connected and accessible.")
        return

    # Request camera to use target frame size (may be ignored on some systems; we also resize in the code)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_H)

    # Initialize HandTracker with default green HSV range
    tracker = HandTracker(
        hsv_lower=(0, 20, 70),
        hsv_upper=(25, 255, 255),
        frame_size=(FRAME_W, FRAME_H),
        min_contour_area=200,
    )

    prev_time = time.time()
    font = cv2.FONT_HERSHEY_SIMPLEX

    print("Press 'q' to quit, 'm' to toggle mask, WASD to move the rectangle.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("WARNING: Empty frame received from webcam.")
                break

            # Process frame to find hand (with its own overlays)
            processed_frame, centroid, contour, bbox = tracker.process_frame(frame, draw_overlays=True)

            # Update rect tuple each frame
            rect = (rect_x1, rect_y1, rect_x2, rect_y2)

            # Compute distance and classify
            if centroid is None:
                d = None
                state = 'SAFE'
            else:
                d = distance_point_to_rect(centroid, rect)
                state = classify_state(d, hand_present=True)

            # Compute FPS
            current_time = time.time()
            elapsed = current_time - prev_time
            fps = 1.0 / elapsed if elapsed > 0 else 0.0
            prev_time = current_time

            # Start drawing final overlays on a copy
            out = processed_frame.copy()

            # Draw virtual rectangle
            cv2.rectangle(out, (rect_x1, rect_y1), (rect_x2, rect_y2), (200, 200, 200), 2)

            # State colors
            color_safe = (0, 255, 0)
            color_warn = (0, 255, 255)
            color_danger = (0, 0, 255)

            # Info when hand not detected
            if centroid is None:
                state_text = "Hand not detected"
                cv2.putText(out, state_text, (10, 30), font, 0.6, (200, 200, 200), 2, cv2.LINE_AA)

            # State display at top-left
            if state == 'SAFE':
                cv2.putText(out, 'SAFE', (10, 70), font, 1.5, color_safe, 3, cv2.LINE_AA)
            elif state == 'WARNING':
                cv2.putText(out, 'WARNING', (10, 70), font, 1.5, color_warn, 3, cv2.LINE_AA)
            elif state == 'DANGER':
                cv2.putText(out, 'DANGER', (10, 70), font, 1.5, color_danger, 4, cv2.LINE_AA)
                # Additionally draw the required "DANGER DANGER" large centered red text
                center_text = "DANGER DANGER"
                (tw, th), _ = cv2.getTextSize(center_text, font, 2.0, 6)
                cx_text = int((FRAME_W - tw) / 2)
                cy_text = int((FRAME_H + th) / 2)
                cv2.putText(out, center_text, (cx_text, cy_text), font, 2.0, color_danger, 6, cv2.LINE_AA)

            # Distance overlay (if available)
            if d is None:
                dist_text = "Distance: N/A"
            else:
                dist_text = f"Distance: {int(round(d))} px"
            cv2.putText(out, dist_text, (10, FRAME_H - 20), font, 0.7, (230, 230, 230), 2, cv2.LINE_AA)

            # FPS overlay
            fps_text = f"FPS: {fps:.1f}"
            cv2.putText(out, fps_text, (FRAME_W - 150, 30), font, 0.7, (200, 200, 200), 2, cv2.LINE_AA)

            # Show final frame
            cv2.imshow("Hand Tracker - Virtual Boundary", out)

            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break
            elif key == ord('m'):
                # Toggle mask debug
                tracker.set_show_mask(not tracker.show_mask)
            elif key in (ord('w'), ord('a'), ord('s'), ord('d')):
                # Move rectangle slightly; keep it within frame bounds
                step = 10
                if key == ord('w'):
                    rect_y1 -= step
                    rect_y2 -= step
                elif key == ord('s'):
                    rect_y1 += step
                    rect_y2 += step
                elif key == ord('a'):
                    rect_x1 -= step
                    rect_x2 -= step
                elif key == ord('d'):
                    rect_x1 += step
                    rect_x2 += step

                # Clamp within frame
                rect_x1 = clamp(rect_x1, 0, FRAME_W - 1)
                rect_x2 = clamp(rect_x2, 1, FRAME_W)
                rect_y1 = clamp(rect_y1, 0, FRAME_H - 1)
                rect_y2 = clamp(rect_y2, 1, FRAME_H)

    finally:
        # Clean up
        cap.release()
        cv2.destroyAllWindows()
        print("Exited and resources released.")


if __name__ == "__main__":
    main()
