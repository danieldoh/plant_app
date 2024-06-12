import numpy as np
import math
import cv2
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