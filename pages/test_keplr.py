import streamlit as st
import pandas as pd
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static

st.set_page_config(layout="wide")

st.title("Kakao Tile + kepler.gl (Streamlit) 예제")

# 샘플 데이터 (서울 시청 한 점)
df = pd.DataFrame(
    {
        "lat": [37.5665],
        "lon": [126.9780],
        "name": ["Seoul City Hall"],
    }
)

# Kakao 타일을 쓰는 kepler.gl config
# ※ url 에는 1단계에서 만든 kakao-style.json 의 주소를 넣어야 합니다.
KEPLER_CONFIG = {
    "version": "v1",
    "config": {
        "visState": {
            "layers": [
                {
                    "id": "point-layer",
                    "type": "point",
                    "config": {
                        "dataId": "points",
                        "label": "Sample Points",
                        "color": [255, 0, 0],
                        "columns": {
                            "lat": "lat",
                            "lng": "lon"
                        },
                        "isVisible": True,
                        "radius": 10
                    },
                    "visualChannels": {
                        "colorField": None,
                        "colorScale": "quantile",
                        "sizeField": None,
                        "sizeScale": "linear"
                    }
                }
            ],
            "interactionConfig": {
                "tooltip": {
                    "fieldsToShow": {
                        "points": ["name", "lat", "lon"]
                    },
                    "enabled": True
                }
            }
        },
        "mapState": {
            "bearing": 0,
            "dragRotate": False,
            "latitude": 37.5665,
            "longitude": 126.9780,
            "pitch": 0,
            "zoom": 12,
            "isSplit": False
        },
        "mapStyle": {
            # 아래 styleType 은 mapStyles 목록 중 하나 id 와 맞추면 됩니다.
            "styleType": "kakao",
            "mapStyles": [
                {
                    "id": "kakao",
                    "label": "Kakao Map",
                    "url": "https://raw.githubusercontent.com/<YOUR_GITHUB_ID>/<REPO>/main/kakao-style.json"  # <- 수정
                }
            ]
        }
    }
}

# keplergl 객체 생성
kepler_map = KeplerGl(
    height=600,
    data={"points": df},
    config=KEPLER_CONFIG
)

# Streamlit 에 렌더링
keplergl_static(kepler_map, center_map=True)