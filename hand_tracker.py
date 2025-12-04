"""
hand_tracker.py

Contains HandTracker class that performs color-based hand detection using HSV thresholding,
morphological cleaning, contour extraction, and computes centroid & bounding box.

Change the HSV range below to match a different glove/color.

Author: Generated for POC (improved version)
"""

import cv2
import numpy as np


class HandTracker:
    def __init__(
        self,
        hsv_lower=(0, 20, 70),
        hsv_upper=(50, 255, 255),
        frame_size=(640, 480),
        min_contour_area=200,
        suppress_top_half=False,
    ):
        """
        Initialize HandTracker.

        Parameters:
        - hsv_lower, hsv_upper: tuples for HSV lower/upper bounds (default tuned for a bright green glove).
            To use a different glove color, change these values. For example:
              - Bright red: lower=(0, 120, 70), upper=(10, 255, 255) and also (170,120,70)-(180,255,255)
              - Bright blue: lower=(100,150,0), upper=(140,255,255)
        - frame_size: (width, height) target size to resize incoming frames for speed.
        - min_contour_area: minimum area to accept a contour as hand (filters small noise).
        """
        # HSV bounds for detection (default: bright green). Change these if using a different glove color.
        self.hsv_lower = np.array(hsv_lower, dtype=np.uint8)
        self.hsv_upper = np.array(hsv_upper, dtype=np.uint8)

        self.frame_width = frame_size[0]
        self.frame_height = frame_size[1]
        self.min_contour_area = min_contour_area

        # Kernel for morphological operations
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

        # Debug flag for showing mask
        self.show_mask = False

    def set_show_mask(self, flag: bool):
        """Enable/disable real-time display of the segmentation mask."""
        self.show_mask = bool(flag)

    def process_frame(self, frame, draw_overlays=True):
        """
        Process a BGR frame to detect hand region.

        Inputs:
        - frame: BGR image from cv2.VideoCapture
        - draw_overlays: if True, returns a copy of frame with contour, bbox and centroid drawn

        Returns tuple:
        - out_frame: annotated BGR frame (or original resized frame if draw_overlays=False)
        - centroid: (cx, cy) integer tuple in pixel coordinates relative to the returned frame, or None if not found
        - largest_contour: contour array of the largest detected contour or None
        - bbox: (x, y, w, h) bounding box of the largest contour or None
        """
        # Resize for faster processing and consistent coordinates
        frame_resized = cv2.resize(frame, (self.frame_width, self.frame_height))

        # Slight blur to reduce noise and flickering
        blurred = cv2.GaussianBlur(frame_resized, (7, 7), 0)

        out_frame = frame_resized.copy()

        # Convert to HSV
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # Threshold HSV to get only the chosen color
        mask = cv2.inRange(hsv, self.hsv_lower, self.hsv_upper)

        mask[: self.frame_height // 2, :] = 0   # ignore top half (face & shirt)
        mask[:, : self.frame_width // 3] = 0   # ignore left side where shirt appears

        # Morphological operations to reduce noise
        mask = cv2.erode(mask, self.kernel, iterations=1)
        mask = cv2.dilate(mask, self.kernel, iterations=2)

        # Show mask for debugging if enabled
        if self.show_mask:
            cv2.imshow("Segmentation Mask", mask)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            # No contours found
            return out_frame, None, None, None

        # Select largest contour by area
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        if area < self.min_contour_area:
            # Contour too small; treat as not found
            return out_frame, None, None, None

        # Optional: contour simplification for stability / slight performance gain
        epsilon = 0.01 * cv2.arcLength(largest_contour, True)
        largest_contour = cv2.approxPolyDP(largest_contour, epsilon, True)

        # Bounding box
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Compute centroid using moments
        M = cv2.moments(largest_contour)
        if M.get("m00", 0) == 0:
            # Degenerate case
            return out_frame, None, largest_contour, (x, y, w, h)

        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        # Draw overlays on out_frame if requested
        if draw_overlays:
            # Contour
            cv2.drawContours(out_frame, [largest_contour], -1, (255, 0, 0), 2)  # blue contour

            # Bounding box
            cv2.rectangle(out_frame, (x, y), (x + w, y + h), (255, 255, 0), 2)  # cyan bbox

            # Centroid
            cv2.circle(out_frame, (cx, cy), 5, (0, 0, 255), -1)  # red centroid

        return out_frame, (cx, cy), largest_contour, (x, y, w, h)
