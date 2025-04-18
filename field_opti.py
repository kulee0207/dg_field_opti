import streamlit as st
import pandas as pd
from haversine import haversine
import folium as g
import numpy as np
import random
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d.art3d import Poly3DCollection



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

def compute_coverage_with_horizontal(H_s, H_r, D, beamwidth_v_deg, beamwidth_h_deg, show_plot=True):
    margin = beamwidth_v_deg / 2 + 1
    tilt_range = np.linspace(-90 + margin, 90 - margin, 1000)
    coverages = []
    best_data = {}
 
    tops = []
    bottoms = []
 
    max_v_coverage = 0
    # best_tilt = None
    # best_top = best_bottom = None
 
    for tilt in tilt_range:
        center_rad = np.radians(tilt)
        half_v_rad = np.radians(beamwidth_v_deg / 2)
 
        upper_rad = center_rad + half_v_rad
        lower_rad = center_rad - half_v_rad
 
        y_upper = H_s + np.tan(upper_rad) * D
        y_lower = H_s + np.tan(lower_rad) * D
 
        y_max = min(max(y_upper, y_lower), H_r)
        y_min = max(min(y_upper, y_lower), 0)
 
        coverage = y_max - y_min
        coverages.append(coverage)
        tops.append(y_max)
        bottoms.append(y_min)
        if coverage > best_data.get("max_v_coverage",0):
            best_data = {
                "max_v_coverage" : round(coverage,2),
                "best_tilt_deg" : round(-tilt,0),
                "coverage_top_m" : round(y_max,2),
                "coverage_bottom_m" : round(y_min,2),
                "main_beam_height" : round(H_s +np.tan(center_rad)*D,2),
            }
    coverages = np.array(coverages)
    valid_idx = coverages > 0
    tilt_range_valid = tilt_range[valid_idx]
    if show_plot:
        plt.figure(figsize=(10, 5))
        plt.plot(-tilt_range, coverages)
        plt.axvline(best_data["best_tilt_deg"], color='red', linestyle='--', label=f"Best Tilt = {-best_data['best_tilt_deg']:.0f}°")
        plt.axhline(best_data["max_v_coverage"], color='blue', linestyle='--', label=f"Max Verticla_Coverage = {best_data['max_v_coverage']:.2f}°")
        plt.title("Tilt Angle vs. Vertical Coverage Length")
        plt.xlabel("Tilt Angle (°)")
        plt.ylabel("Vertical Coverage (m)")
        plt.ylim(bottom=0)
        plt.xlim(-tilt_range_valid[0],-tilt_range_valid[-1])
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
        fig = plt.gcf()
        plt.close()
        half_h_rad = np.radians(beamwidth_h_deg / 2)
        horizontal_coverage = 2 * D * np.tan(half_h_rad)
        best_data["horizontal_coverage_m"] = round(horizontal_coverage,2)
        return best_data, fig

    # 수평 커버리지 계산
    half_h_rad = np.radians(beamwidth_h_deg / 2)
    horizontal_coverage = 2 * D * np.tan(half_h_rad)
    best_data["horizontal_coverage_m"] = round(horizontal_coverage,2)
    return best_data
 
def plot_3d_beam_coverage_with_volume(H_s, H_r, D, tilt_deg, beamwidth_v_deg, beamwidth_h_deg):
    center_rad = np.radians(tilt_deg)
    half_v_rad = np.radians(beamwidth_v_deg / 2)
    half_h_rad = np.radians(beamwidth_h_deg / 2)
 
    # 빔 중심 높이 및 수직 경계
    center_y = H_s + np.tan(center_rad) * D
    y_upper = min(H_s + np.tan(center_rad + half_v_rad) * D, H_r)
    y_lower = max(H_s + np.tan(center_rad - half_v_rad) * D, 0)
 
    # 수평 커버리지 좌우 폭 (Y축 방향)
    horizontal_half = D * np.tan(half_h_rad)
 
    # 수신면 사각형 꼭짓점 4개
    far_plane = [
        [D, -horizontal_half, y_lower],
        [D, -horizontal_half, y_upper],
        [D, horizontal_half, y_upper],
        [D, horizontal_half, y_lower]
    ]
 
    # 송신점 위치 (x=0, y=0, z=H_s)
    source_point = [0, 0, H_s]
 
    # 빔 벌룬(사각뿔) 면들 정의
    faces = [
        [source_point, far_plane[0], far_plane[1]],  # 왼쪽면
        [source_point, far_plane[1], far_plane[2]],  # 윗면
        [source_point, far_plane[2], far_plane[3]],  # 오른쪽면
        [source_point, far_plane[3], far_plane[0]],  # 아랫면
        far_plane  # 수신면 자체 (사각형)
    ]
 
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111, projection='3d')
 
    # 송신 건물
    ax.bar3d(0, -1, 0, 2, 2, H_s, color='blue', alpha=0.5, label="Tx Building")
    # 수신 건물
    ax.bar3d(D, -2, 0, 2, 4, H_r, color='green', alpha=0.5, label="Rx Building")
 
    # 빔 볼륨 (사각뿔)
    beam_poly = Poly3DCollection(faces, color='orange', alpha=0.3)
    ax.add_collection3d(beam_poly)
 
    # 축 및 범위 설정
    ax.set_xlabel("X (Distance)")
    ax.set_ylabel("Y (Horizontal Spread)")
    ax.set_zlabel("Height (m)")
    ax.set_title(f"3D Beam Volume\nTilt: {-tilt_deg:.0f}°, H Beamwidth: {beamwidth_h_deg}°, V Beamwidth: {beamwidth_v_deg}°")
    ax.set_xlim(0, D + 20)
    ax.set_ylim(-horizontal_half * 2, horizontal_half * 2)
    ax.set_zlim(0, max(H_r, y_upper) + 10)
    ax.legend()
    plt.tight_layout()
    plt.show()
    fig = plt.gcf()
    plt.close()
    return fig
 
# 실행 예시
# params = compute_coverage_with_horizontal(
#     H_s=18,
#     H_r=30,
#     D=60,
#     beamwidth_v_deg=17,
#     beamwidth_h_deg=65,
#     show_plot=True
# )
 
# plot_3d_beam_coverage_with_volume(
#     H_s=18,
#     H_r=30,
#     D=60,
#     tilt_deg=params['best_tilt_deg'],
#     beamwidth_v_deg=17,
#     beamwidth_h_deg=65
# )
 
# print(params)




st.title("최적화 도구")
col1, col2 = st.columns(2)

row2_col1, row2_col2, row2_col3 = st.columns(3)

with col1:
    st.image("images/mainbeam_calcul.jpg", caption="Main Beam 수직 커버리지 게산")
with col2:
    st.image("images/AAU_Beamshape.JPG", caption="AAU Type 별 Beam Shape")


with row2_col1:
    with st.expander("최적 tilt 계산"):
        target_bld_height = st.number_input("Target 서비스 건물 높이(m) : ", key='unique_key_301')
        base_station_height = st.number_input("중계기 시설 높이(m) ", key='unique_key_303')
        distance = st.number_input("두 건물 사이의 거리(m) ", key='unique_key_302')
        beamwidth_v_deg = st.number_input("수직 빔폭(도) ", key='unique_key_304')
        beamwidth_h_deg = st.number_input("수평 빔폭(도) ", key='unique_key_305')
        if st.button("최적 Tilt 반환", key="unique_key_3"):
            params, fig_2d = compute_coverage_with_horizontal(
                H_s = base_station_height,
                H_r = target_bld_height,
                D = distance,
                beamwidth_v_deg = beamwidth_v_deg,
                beamwidth_h_deg = beamwidth_h_deg,
                show_plot=True
                )
            fig_3d = plot_3d_beam_coverage_with_volume(
                H_s = base_station_height,
                H_r = target_bld_height,
                D = distance,
                tilt_deg=params['best_tilt_deg'],
                beamwidth_v_deg = beamwidth_v_deg,
                beamwidth_h_deg = beamwidth_h_deg
                )
            st.write(params)
            st.pyplot(fig_2d)
            st.pyplot(fig_3d)

with row2_col2:
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


