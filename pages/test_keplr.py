import streamlit as st
import pandas as pd
import pydeck as pdk

# 1) 위경도 데이터
df = pd.DataFrame({
    "lat": [37.5665, 37.57],
    "lon": [126.9780, 126.98],
})

# 2) Kakao 또는 VWorld 타일 URL
KAKAO_KEY = "df7524b09d181806b21d9780fd224a06"
kakao_tile_url = f"https://dapi.kakao.com/v2/map/tile/{{z}}/{{x}}/{{y}}.png?appkey={KAKAO_KEY}"


# 3) TileLayer: 베이스맵
kakao_layer = pdk.Layer(
    "TileLayer",
    data=None,
    min_zoom=0,
    max_zoom=19,
    tile_size=256,
    get_tile_data=kakao_tile_url,  # <-- 여기만 VWorld로 바꾸면 VWorld 베이스맵
    opacity=1.0,
)

# 4) 데이터 레이어 (예: Scatterplot)
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position="[lon, lat]",
    get_radius=200,
    get_fill_color="[255, 0, 0, 200]",
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=df["lat"].mean(),
    longitude=df["lon"].mean(),
    zoom=12,
    pitch=0,
)

deck = pdk.Deck(
    layers=[kakao_layer, scatter_layer],
    initial_view_state=view_state,
    map_style=None  # <-- Mapbox 스타일 OFF, 타일만 사용
)

st.pydeck_chart(deck)