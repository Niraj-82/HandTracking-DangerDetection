"""
state_logic.py

Contains functions to compute distance from a point to a rectangle and classify state
according to the precise rules specified.

Distance rules:
- If point inside rectangle (including edges): distance = 0
- Else if horizontally aligned, distance = vertical gap to top/bottom edge
- Else if vertically aligned, distance = horizontal gap to left/right edge
- Else (diagonally outside): distance = Euclidean distance to the nearest rectangle corner

State classification thresholds:
- SAFE: d > 120
- WARNING: 60 < d <= 120
- DANGER: d <= 60 OR d == 0
"""

import math


def distance_point_to_rect(pt, rect):
    """
    Compute minimum distance from point pt to rectangle rect.

    Parameters:
    - pt: (cx, cy)
    - rect: (rect_x1, rect_y1, rect_x2, rect_y2) where rect_x2 > rect_x1, rect_y2 > rect_y1

    Returns:
    - distance (float). 0 if inside or on edge.
    """
    cx, cy = pt
    rx1, ry1, rx2, ry2 = rect

    # Check if inside (including edges)
    if rx1 <= cx <= rx2 and ry1 <= cy <= ry2:
        return 0.0

    # If horizontally between left and right edges but vertically outside
    if rx1 <= cx <= rx2:
        if cy < ry1:
            return float(ry1 - cy)
        else:
            return float(cy - ry2)

    # If vertically between top and bottom edges but horizontally outside
    if ry1 <= cy <= ry2:
        if cx < rx1:
            return float(rx1 - cx)
        else:
            return float(cx - rx2)

    # Diagonally outside -> distance to nearest corner
    corners = [(rx1, ry1), (rx1, ry2), (rx2, ry1), (rx2, ry2)]
    dists = [math.hypot(cx - x, cy - y) for (x, y) in corners]
    return float(min(dists))


def classify_state(distance, hand_present):
    """
    Classify state into 'SAFE', 'WARNING', 'DANGER' based on distance d and whether hand is present.

    Parameters:
    - distance: float distance in pixels (from distance_point_to_rect)
    - hand_present: bool (False if no hand detected)

    Returns:
    - state: string 'SAFE'|'WARNING'|'DANGER'
    """
    # If hand not detected, default to SAFE
    if not hand_present:
        return 'SAFE'

    d = float(distance)

    # DANGER if d <= 60 OR d == 0 (explicitly included)
    if d == 0.0 or d <= 60.0:
        return 'DANGER'
    # WARNING: 60 < d <= 120
    if 60.0 < d <= 120.0:
        return 'WARNING'
    # SAFE: d > 120
    if d > 120.0:
        return 'SAFE'

    # Fallback (should not be reached)
    return 'SAFE'
