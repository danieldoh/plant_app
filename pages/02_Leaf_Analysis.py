import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

import io
import time
import numpy as np
from PIL import Image
from src.utils import two_points_distance
from datetime import datetime

st.set_page_config(
    page_title="Leaf Analysis",
    page_icon="🍃",
    layout='wide',
)

st.title("Leaf Analysis")