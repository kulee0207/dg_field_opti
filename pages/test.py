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
initial_value = (today,today)

d = st.date_input(
    "최적화 전 일자 조회 기간",
    value=initial_value,
    min_value=jan_1,
    max_value=dec_31,
    format="MM.DD.YYYY",
)
if d == initial_value:
    d = (None,None)

dates = [for date in d]
st.write(dates[0])