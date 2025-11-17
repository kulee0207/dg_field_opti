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
from keplergl import KeplerGl

def rsr_to_color(value):
    if value >= -80:
        return [0, 0, 255]
    elif value >= -90:
        return [0,255,0]
    elif value >= -105:
        return [255,255,0]
    else:
        return [255,0,0]

def create_rec(lat, lon):
    return [
        [lon-0.001/2, lat-0.001/2],
        [lon-0.001/2, lat+0.001/2],
        [lon+0.001/2, lat+0.001/2],
        [lon+0.001/2, lat-0.001/2]
    ]
    


df = pd.DataFrame({
    "lat": [37.5665, 37.5670, 37.5675],
    "lon": [126.9780, 126.9790, 126.9800],
    "rsrp": [-75, -88, -102],
    "sinr": [20,15,8]
})

df["color"] = df["rsrp"].apply(rsrp_to_color)
df["polygon"] = df.apply(lambda row : create_rectangle(row["lat"], row["lon"]), axis=1)

polygon_layer = pdk.Layer(
    "PolygonLayer",
    df,
    get_polygon="polygon",
    get_fill_color="color",
    get_line_color=[0,0,0],
    line_width_min_pixels=1,
    pickable=True,
    auto_highlight=True
)

api_key = "df7524b09d181806b21d9780fd224a06"
kakao_tile_url = f"https://dapi.kakao.com/v2/map/tile/{{z}}/{{x}}/{{y}}.png?appkey={api_key}"

