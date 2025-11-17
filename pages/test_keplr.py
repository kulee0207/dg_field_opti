import streamlit as st
import pandas as pd
import pydeck as pdk

# ----------------------------------
# 0. 예시 데이터 (실제에선 df 불러오면 됨)
# ----------------------------------
# df = pd.read_csv("your_file.csv")  # 실제 데이터
# df에는 반드시 lat, lon 컬럼이 있어야 합니다.

# 여기서는 샘플만
import numpy as np
n = 30000
center_lat, center_lon = 37.5665, 126.9780  # 서울
df = pd.DataFrame({
    "lat": center_lat + (np.random.rand(n) - 0.5) * 2.0,   # 대충 한국 범위
    "lon": center_lon + (np.random.rand(n) - 0.5) * 2.0,
    "value": np.random.randint(0, 100, n)
})

# ----------------------------------
# 1. 초기 뷰 (한국 중심)
# ----------------------------------
view_state = pdk.ViewState(
    latitude=df["lat"].mean(),
    longitude=df["lon"].mean(),
    zoom=6,
    pitch=0,
    bearing=0,
)

# ----------------------------------
# 2. ScatterplotLayer 정의
# ----------------------------------
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position="[lon, lat]",       # lon, lat 순서
    get_radius=200,                  # 점 반경 (m 단위 느낌)
    get_fill_color="[255, 140, 0, 160]",  # RGBA
    pickable=True,
)

# ----------------------------------
# 3. Deck 객체 생성 및 스트림릿 출력
# ----------------------------------
deck = pdk.Deck(
    layers=[scatter_layer],
    initial_view_state=view_state,
    map_style="light",   # 기본 Mapbox light 스타일 (한국 모양 충분히 나옵니다)
    tooltip={"text": "lat: {lat}\nlon: {lon}\nvalue: {value}"}
)

st.title("한국 위경도 데이터 시각화 (pydeck Scatterplot)")
st.pydeck_chart(deck)