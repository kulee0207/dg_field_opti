import streamlit as st
import pandas as pd
from haversine import haversine
import folium as g
import numpy as np
import random
import matplotlib.pyplot as plt
import math




st.set_page_config(
    page_title = "Field Optimization",
    layout = "wide"
)

def calculate_tilt(distance, base_station_height, target_hieght, vertical_beamwidth):
    tilt_radians = math.atan((target_height - base_station_height) / distance)

    tilt_degrees = math.degrees(tilt_radians)

    if target_height > base_station_height:
        tilt = -abs(tilt_degrees)

    else:
        tilt = abs(tilt_degrees)
    
    vertical_beamwidth_radias = math.radians(vertical_beamwidth)
    min_height = base_station_height + distance*math.tan(tilt_radians - vertical_beamwidth_radias / 2)
    max_height = base_station_height + distance*math.tan(tilt_radians + vertical_beamwidth_radias / 2)
    min_height = max(0,min_height)
    verti_coverage_range = (min_height, max_height)

    return tilt, verti_coverage_range

def calculate_horizontal_coverage(distance_between_buildings, horizontal_beamwidth, target_height, base_station_height):

    height_difference = abs(target_height - base_station_height)
    distance_to_target = math.sqrt(distance_between_buildings**2 + height_difference**2)

    beamwidth_radians = math.radians(horizontal_beamwidth)

    left_distance = distance*math.tan(-horizontal_beamwidth/2)
    right_distance = distance*math.tan(horizontal_beamwidth/2)

    horizon_cover_range = abs(left_distance-right_distance)
    return horizon_cover_range

def calculate_coverage_from_tilt(distance, base_station_height, tilt, vertical_beamwidth, horizontal_beamwidth):
    tilt_radians = math.radians(tilt)

    vertical_beamwidth_radians = math.radians(vertical_beamwidth)
    horizontal_beamwidth_radians = math.radians(horizontal_beamwidth)

    min_height = base_station_height + distance*math.tan(tilt_radians - vertical_beamwidth_radians/2)
    max_height = base_station_height + distance*math.tan(tilt_radians + vertical_beamwidth_radians/2)
    min_height = max(0, min_height)
    verti_coverage_range = (min_height, max_height)

    left_distance = distance*math.tan(-horizontal_beamwidth_radians/2)
    right_distance = distance*math.tan(horizontal_beamwidth_radians/2)
    horizon_coverage_range = abs(left_distance-right_distance)

    return verti_coverage_range, horizon_coverage_range

st.title("최적화 도구")
col1, col2 = st.columns(2)

with col1:
    with st.expander("틸트 및 커버리지 계산"):
        target_height = st.number_input("Main Beam target 높이 (m) : ", key='unique_key_101')
        distance = st.number_input("두 건물 사이의 거리(m): ", key='unique_key_102')
        base_station_height = st.number_input("중계기 시설 높이 (m): ", key='unique_key_103')
        vertical_beamwidth = st.number_input("수직 빔폭 (도): ", key='unique_key_104')
        horizontal_beamwidth = st.number_input("수평 빔폭 (도): ", key='unique_key_105')
        if st.button("틸트 계산하기", key = "unique_key_1"):
            tilt, verti_cov_range = calculate_tilt(distance, base_station_height, target_height, vertical_beamwidth)
            horizon_cov_range = calculate_horizontal_coverage(distance, horizontal_beamwidth, target_height, base_station_height)

            st.write(f"계산된 틸트 값 : {tilt:.0f}도")
            st.write(f"메인 빔이 커버할 수 있는 수직 범위 : {verti_cov_range[0]:.2f}m ~ {verti_cov_range[1]:.2f}m")
            st.write(f"메인 빔이 커버할 수 있는 좌우 범위 : {horizon_cov_range:.2f}m")


# def main():
#     st.title('Hello')


# if __name__=='__main__':
#     main()

