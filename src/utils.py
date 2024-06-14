import numpy as np
import math
import csv

from PIL import Image
from collections import Counter
import matplotlib.pyplot as plt
import colorsys

def two_points_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    return distance

def angle_calculation(p1, p2, p3):
    p1_np = np.array(p1)
    p2_np = np.array(p2)
    p3_np = np.array(p3)

    vec1 = p2_np - p1_np
    vec2 = p3_np - p1_np

    dot_product = np.dot(vec1, vec2)
    magnitude_1 = np.linalg.norm(vec1)
    magnitude_2 = np.linalg.norm(vec2)

    cos_theta = dot_product / (magnitude_1 * magnitude_2)

    angle_rad = np.arccos(cos_theta)
    angle_deg = np.degrees(angle_rad)

    return angle_deg