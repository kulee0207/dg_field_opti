import streamlit as st
import pandas as pd
from haversine import haversine
import folium as g
import numpy as np
import random
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import datetime


today = datetime.datetime.now()
last_year = today.year - 1
this_year = today.year
jan_1 = datetime.date(last_year, 1, 1)
dec_31 = datetime.date(this_year, 12, 31)

d = st.date_input(
    "Select your vacation for next year",
    (jan_1, datetime.date(next_year, 1, 7)),
    jan_1,
    dec_31,
    format="MM.DD.YYYY",
)
dates = [date.strftime("%Y%m%d") for date in d]
st.write(dates)