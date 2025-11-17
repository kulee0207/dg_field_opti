
import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np

st.set_page_config(layout="wide")

st.title("Kakao TileLayer + ScatterplotLayer 테스트")

# ------------------------------
# 1) 예시 대량 데이터 생성 (2~5만 포인트)
# ------------------------------
N = 20000
center_lat, center_lon = 37.5665, 126.9780  # 서울 중심

df = pd.DataFrame({
    "lat": center_lat + (np.random.rand(N) - 0.5) * 2.0,
    "lon": center_lon + (np.random.rand(N) - 0.5) * 2.0,
    "value": np.random.randint(0, 100, N),
})

# ------------------------------
# 2) Kakao XYZ Tile URL
# ------------------------------
KAKAO_REST_API_KEY = "df7524b09d181806b21d9780fd224a06"

kakao_tile_url = (
    f"https://dapi.kakao.com/v2/map/tile/{{z}}/{{x}}/{{y}}.png"
    f"?appkey={KAKAO_REST_API_KEY}"
)

# ------------------------------
# 3) pydeck TileLayer
# ------------------------------
kakao_layer = pdk.Layer(
    "TileLayer",
    data=None,
    min_zoom=0,
    max_zoom=18,
    tile_size=256,
    get_tile_data=kakao_tile_url,
    opacity=1.0,
)

# ------------------------------
# 4) Scatterpoint 레이어
# ------------------------------
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position="[lon, lat]",
    get_radius=200,               # m 단위 대략
    get_fill_color="[255, 0, 0, 160]",
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=df["lat"].mean(),
    longitude=df["lon"].mean(),
    zoom=10,
    pitch=0,
)

deck = pdk.Deck(
    layers=[kakao_layer, scatter_layer],
    initial_view_state=view_state,
    map_style=None,               # Mapbox 스타일 끔
    tooltip={"text": "lat: {lat}\nlon: {lon}\nvalue: {value}"},
)

st.pydeck_chart(deck)