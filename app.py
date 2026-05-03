import numpy as np
import folium
import random
import requests
import time
import streamlit as st
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# ==========================================
# STREAMLIT CONFIG
# ==========================================
st.set_page_config(layout="wide")

geolocator = Nominatim(user_agent="movin_healing_v12_padding_fix")

# ==========================================
# GIỮ NGUYÊN CSS
# ==========================================
st.markdown("""
<style>
    .container { width:100% !important; }
    .app-container {
        background-color: #db2777;
        padding: 40px 20px;
        width: 100vw; min-height: 100vh;
        margin: -20px;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        color: white;
        display: flex; flex-direction: column; align-items: center;
    }
    .inner-wrapper { width: 100%; max-width: 500px; }
    .title-white { text-align: center; font-size: 38px; font-weight: 800; color: white; margin-bottom: 5px; }
    .slogan-white { text-align: center; font-size: 16px; color: #fce7f3; margin-bottom: 30px; }
    
    .input-group {
        background: rgba(255, 255, 255, 0.15);
        padding: 20px; border-radius: 20px; margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    .label-white { color: white; font-size: 13px; font-weight: bold; margin-bottom: 8px; display: block; }
    
    .btn-healing {
        background: white !important; color: #db2777 !important; font-weight: 900 !important;
        height: 60px !important; border-radius: 25px !important; width: 100% !important;
        border: none !important; font-size: 18px !important; cursor: pointer;
    }
    
    .driver-info-card {
        background: white; color: #1f2937; border-radius: 20px; 
        padding: 35px;
        margin-top: 20px; border-left: 10px solid #fb7185; width: 100%;
    }
    .price-tag { 
        font-size: 30px; color: #be185d; font-weight: 800; 
        text-align: right; margin-top: 20px; border-top: 1px dashed #fce7f3; 
        padding-top: 15px; 
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HÀM GIỮ NGUYÊN
# ==========================================
def get_route(start, end):
    try:
        url = f"http://router.project-osrm.org/route/v1/driving/{start[1]},{start[0]};{end[1]},{end[0]}?overview=full&geometries=geojson"
        res = requests.get(url, timeout=5).json()
        return [(c[1], c[0]) for c in res['routes'][0]['geometry']['coordinates']], res['routes'][0]['distance'] / 1000
    except:
        return [start, end], geodesic(start, end).km

# ==========================================
# UI
# ==========================================
st.markdown('<div class="app-container">', unsafe_allow_html=True)
st.markdown('<div class="inner-wrapper">', unsafe_allow_html=True)

st.markdown('<div class="title-white">🚗 Movin Healing</div>', unsafe_allow_html=True)
st.markdown('<div class="slogan-white">Chuyến đi không chỉ là di chuyển...</div>', unsafe_allow_html=True)

# INPUT
in_don = st.text_input("Điểm đón")
in_den = st.text_input("Điểm đến")

# BUTTON
if st.button("Bắt đầu hành trình"):
    
    if not in_don or not in_den:
        st.markdown("<b style='color:white;'>Vui lòng nhập lộ trình!</b>", unsafe_allow_html=True)
    else:
        try:
            loc1 = geolocator.geocode(in_don)
            loc2 = geolocator.geocode(in_den)

            start = (loc1.latitude, loc1.longitude)
            end = (loc2.latitude, loc2.longitude)

            route, distance = get_route(start, end)

            # MAP
            m = folium.Map(location=start, zoom_start=13)
            folium.Marker(start, tooltip="Điểm đón").add_to(m)
            folium.Marker(end, tooltip="Điểm đến").add_to(m)
            folium.PolyLine(route, color="pink", weight=6).add_to(m)

            st_folium(m, width=700, height=500)

            # GIẢ LẬP TÀI XẾ
            driver_name = random.choice(["Anh Tuấn", "Chị Linh", "Anh Hùng", "Chị Mai"])
            rating = round(random.uniform(4.5, 5.0), 1)
            price = int(distance * 15000)

            st.markdown(f"""
            <div class="driver-info-card">
                <h3>🚕 Tài xế: {driver_name}</h3>
                <p>⭐ Đánh giá: {rating}</p>
                <p>📍 Khoảng cách: {distance:.2f} km</p>
                <div class="price-tag">{price:,} VND</div>
            </div>
            """, unsafe_allow_html=True)

        except:
            st.markdown("<b style='color:white;'>Không tìm thấy địa điểm!</b>", unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)
