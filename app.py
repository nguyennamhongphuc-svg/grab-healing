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
# CONFIG
# ==========================================
st.set_page_config(layout="wide")
geolocator = Nominatim(user_agent="movin_healing_v12_padding_fix")

# ==========================================
# CSS (FIX NỀN HỒNG CHỮ TRẮNG)
# ==========================================
st.markdown("""
<style>
    /* Ép nền toàn bộ trang web màu hồng */
    .stApp {
        background-color: #db2777 !important;
    }
    .app-container {
        padding: 40px 20px;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        color: white;
        display: flex; flex-direction: column; align-items: center;
    }
    /* Chỉnh chữ của các label input sang màu trắng */
    .stMarkdown p, label, .stSelectbox label, .stTextInput label {
        color: white !important;
    }
    .inner-wrapper { width: 100%; max-width: 500px; }
    .title-white { text-align: center; font-size: 38px; font-weight: 800; color: white; margin-bottom: 5px; }
    .slogan-white { text-align: center; font-size: 16px; color: #fce7f3; margin-bottom: 30px; }
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

st.markdown("<div class='title-white'>Grab Healing 💖</div>", unsafe_allow_html=True)
st.markdown("<div class='slogan-white'>Nơi trái tim được chữa lành sau mọi hành trình</div>", unsafe_allow_html=True)

# INPUT
in_don = st.text_input("📍 Điểm đón hiện tại...")
in_den = st.text_input("📍 Nơi muốn đến...")
dr_mood = st.selectbox("🧠 Tâm trạng", ['Cần tâm sự', 'Cần yên tĩnh', 'Đang rất vui', 'Căng thẳng'])
dr_gender = st.selectbox("👤 Giới tính tài xế", ['Nam', 'Nữ', 'Bất kỳ'])
dr_age = st.selectbox("🎂 Độ tuổi tài xế", ['18-25', '26-35', '36-50'])

# Tạo các vùng trống để cập nhật nội dung mà không bị mất Map
msg_slot = st.empty()
card_slot = st.empty()
map_slot = st.empty()

# ==========================================
# BUTTON
# ==========================================
if st.button("BẮT ĐẦU HÀNH TRÌNH"):

    if not in_don or not in_den:
        st.markdown("<b style='color:white;'>Vui lòng nhập lộ trình!</b>", unsafe_allow_html=True)

    else:
        loc_don = geolocator.geocode(in_don)
        loc_den = geolocator.geocode(in_den)

        if not loc_don or not loc_den:
            st.markdown("<b style='color:white;'>Không tìm thấy địa điểm!</b>", unsafe_allow_html=True)
        else:
            pos_don = (loc_don.latitude, loc_don.longitude)
            pos_den = (loc_den.latitude, loc_den.longitude)

            # ===== GIAI ĐOẠN 1: QUÉT TÀI XẾ =====
            msg_slot.markdown("<p style='text-align:center;'>🔍 <b>Đang quét tần số tài xế phù hợp...</b></p>", unsafe_allow_html=True)

            m1 = folium.Map(location=pos_don, zoom_start=15)
            folium.Marker(pos_don, icon=folium.Icon(color='red', icon='heart', prefix='fa')).add_to(m1)

            drivers_pos = [(pos_don[0] + random.uniform(-0.005, 0.005),
                            pos_don[1] + random.uniform(-0.005, 0.005)) for _ in range(4)]

            for p in drivers_pos:
                folium.Marker(p, icon=folium.Icon(color='blue', icon='car', prefix='fa')).add_to(m1)

            with map_slot:
                st_folium(m1, width=700, height=500, key="map_stage_1")
            
            time.sleep(3) # Đợi để người dùng kịp nhìn thấy xe xung quanh

            # DỮ LIỆU TÀI XẾ
            nearest_driver = drivers_pos[0]
            route_to_user, dist_to_user = get_route(nearest_driver, pos_don)
            route_to_dest, dist_final = get_route(pos_don, pos_den)
            price = 15000 + (dist_final * 12000)

            mood_configs = {
                'Cần tâm sự': ('Trần Minh Anh', 'VinFast VF8', 'Thấu cảm, ấm áp', 'Tài xế như một người bạn thân.'),
                'Cần yên tĩnh': ('Lê Quốc Bảo', 'Toyota Camry', 'Lịch sự, điềm đạm', 'Không gian cực kỳ riêng tư.'),
                'Đang rất vui': ('Nguyễn Hoàng Nam', 'Mazda 6', 'Năng động, hóm hỉnh', 'Chuyến xe đầy tiếng cười!'),
                'Căng thẳng': ('Đặng Mỹ Hạnh', 'Honda Accord', 'Nhẹ nhàng, tinh tế', 'Giúp tôi thư giãn rất nhiều.')
            }

            driver_name, car_model, trait, feedback = mood_configs[dr_mood]
            stars = random.choice(["4.8", "4.9", "5.0"])
            trips = random.randint(150, 450)

            def get_card_html(title, subtitle):
                return f"""
                <div class='driver-info-card'>
                    <div style='display: flex; justify-content: space-between;'>
                        <b style='color:#db2777; font-size:22px;'>{title} 💖</b>
                        <span style='color:#f59e0b; font-weight:bold;'>⭐ {stars}</span>
                    </div>
                    <div style='margin-top:15px; font-size:16px; color:#1f2937; line-height: 1.6;'>
                        👤 Tài xế: <b>{driver_name}</b> ({dr_age} | {dr_gender})<br>
                        🚗 Xe: <b>{car_model}</b><br>
                        ✨ Tính cách: <i>{trait}</i> | 🚗 Số chuyến: {trips}<br>
                        💬 Feedback: "{feedback}"
                    </div>
                    <div class='price-tag'>{price:,.0f} VNĐ</div>
                </div>
                <p style='text-align:center; margin-top:20px; color: white; font-weight: 800;'>{subtitle}</p>
                """

            # ===== GIAI ĐOẠN 2: TÀI XẾ ĐANG ĐẾN =====
            msg_slot.empty() # Xóa dòng quét tần số
            card_slot.markdown(get_card_html("KẾT NỐI THÀNH CÔNG", f"Tài xế đang đến đón ({dist_to_user:.2f} km)..."), unsafe_allow_html=True)

            m2 = folium.Map(location=pos_don, zoom_start=15)
            folium.PolyLine(route_to_user, color='blue', weight=5).add_to(m2)
            folium.Marker(pos_don, icon=folium.Icon(color='red', icon='heart', prefix='fa')).add_to(m2)
            folium.Marker(nearest_driver, icon=folium.Icon(color='blue', icon='car', prefix='fa')).add_to(m2)

            with map_slot:
                st_folium(m2, width=700, height=500, key="map_stage_2")
            
            time.sleep(4)

            # ===== GIAI ĐOẠN 3: ĐANG DI CHUYỂN =====
            card_slot.empty()
            card_slot.markdown(get_card_html("HÀNH TRÌNH CHỮA LÀNH", f"Đang di chuyển đến điểm đích ({dist_final:.2f} km)..."), unsafe_allow_html=True)

            m3 = folium.Map(location=pos_don, zoom_start=14)
            folium.PolyLine(route_to_dest, color='#db2777', weight=7).add_to(m3)
            folium.Marker(pos_don, icon=folium.Icon(color='red', icon='heart', prefix='fa')).add_to(m3)
            folium.Marker(pos_den, icon=folium.Icon(color='green', icon='flag', prefix='fa')).add_to(m3)

            with map_slot:
                st_folium(m3, width=700, height=500, key="map_stage_3")

st.markdown('</div></div>', unsafe_allow_html=True)
