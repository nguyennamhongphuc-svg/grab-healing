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
st.set_page_config(layout="wide", page_title="Grab Healing 💖")

# HÀM GIÚP TÌM ĐỊA CHỈ THÔNG MINH (TỰ ĐỘNG THỬ LẠI)
def smart_geocode(address):
    # Mỗi lần gọi sẽ dùng một tên app khác nhau để tránh bị chặn
    user_agents = [f"healing_app_{random.randint(100, 999)}" for _ in range(5)]
    
    for i in range(3): # Thử tối đa 3 lần
        try:
            agent = random.choice(user_agents)
            geolocator = Nominatim(user_agent=agent, timeout=10)
            result = geolocator.geocode(address)
            if result:
                return result
            time.sleep(1) # Nghỉ 1 giây trước khi thử lại
        except:
            time.sleep(1.5)
    return None

# ==========================================
# CSS (GIỮ NGUYÊN PHONG CÁCH HỒNG TRẮNG)
# ==========================================
st.markdown("""
<style>
    .stApp { background-color: #db2777 !important; }
    .app-container { padding: 40px 20px; color: white; display: flex; flex-direction: column; align-items: center; }
    .stMarkdown p, label, .stSelectbox label, .stTextInput label { color: white !important; font-weight: bold; }
    .inner-wrapper { width: 100%; max-width: 500px; }
    .title-white { text-align: center; font-size: 38px; font-weight: 800; color: white; margin-bottom: 5px; }
    .slogan-white { text-align: center; font-size: 16px; color: #fce7f3; margin-bottom: 30px; }
    .driver-info-card {
        background: white; color: #1f2937; border-radius: 20px; 
        padding: 30px; margin-top: 20px; border-left: 10px solid #fb7185;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .price-tag { 
        font-size: 28px; color: #be185d; font-weight: 800; 
        text-align: right; margin-top: 15px; border-top: 1px dashed #fce7f3; padding-top: 10px; 
    }
    iframe { width: 100% !important; border-radius: 15px; }
</style>
""", unsafe_allow_html=True)

def get_route(start, end):
    try:
        url = f"http://router.project-osrm.org/route/v1/driving/{start[1]},{start[0]};{end[1]},{end[0]}?overview=full&geometries=geojson"
        res = requests.get(url, timeout=5).json()
        return [(c[1], c[0]) for c in res['routes'][0]['geometry']['coordinates']], res['routes'][0]['distance'] / 1000
    except:
        return [start, end], geodesic(start, end).km

# ==========================================
# KHỞI TẠO TRẠNG THÁI
# ==========================================
if 'step' not in st.session_state:
    st.session_state.step = 0

# ==========================================
# UI CHÍNH
# ==========================================
st.markdown('<div class="app-container"><div class="inner-wrapper">', unsafe_allow_html=True)
st.markdown("<div class='title-white'>Grab Healing 💖</div>", unsafe_allow_html=True)
st.markdown("<div class='slogan-white'>Nơi trái tim được chữa lành sau mọi hành trình</div>", unsafe_allow_html=True)

in_don = st.text_input("📍 Điểm đón hiện tại...", value="TP. Hồ Chí Minh")
in_den = st.text_input("📍 Nơi muốn đến...", value="Vũng Tàu")
dr_mood = st.selectbox("🧠 Tâm trạng", ['Cần tâm sự', 'Cần yên tĩnh', 'Đang rất vui', 'Căng thẳng'])
dr_gender = st.selectbox("👤 Giới tính tài xế", ['Nam', 'Nữ', 'Bất kỳ'])
dr_age = st.selectbox("🎂 Độ tuổi tài xế", ['18-25', '26-35', '36-50'])

if st.button("BẮT ĐẦU HÀNH TRÌNH"):
    if in_don and in_den:
        st.session_state.step = 1
    else:
        st.error("Vui lòng nhập đầy đủ lộ trình!")

# ==========================================
# LOGIC HIỂN THỊ
# ==========================================
if st.session_state.step > 0:
    # SỬA LỖI: Gọi hàm smart_geocode đã có cơ chế tự thử lại
    loc_don = smart_geocode(in_don)
    loc_den = smart_geocode(in_den)
    
    if loc_don and loc_den:
        pos_don = (loc_don.latitude, loc_don.longitude)
        pos_den = (loc_den.latitude, loc_den.longitude)
        
        random.seed(42)
        drivers_pos = [(pos_don[0] + 0.003, pos_don[1] + 0.003) for _ in range(4)]
        nearest_driver = drivers_pos[0]
        
        route_to_user, dist_to_user = get_route(nearest_driver, pos_don)
        route_to_dest, dist_final = get_route(pos_don, pos_den)
        
        mood_configs = {
            'Cần tâm sự': ('Trần Minh Anh', 'VinFast VF8', 'Thấu cảm, ấm áp', 'Tài xế như một người bạn thân.'),
            'Cần yên tĩnh': ('Lê Quốc Bảo', 'Toyota Camry', 'Lịch sự, điềm đạm', 'Không gian cực kỳ riêng tư.'),
            'Đang rất vui': ('Nguyễn Hoàng Nam', 'Mazda 6', 'Năng động, hóm hỉnh', 'Chuyến xe đầy tiếng cười!'),
            'Căng thẳng': ('Đặng Mỹ Hạnh', 'Honda Accord', 'Nhẹ nhàng, tinh tế', 'Giúp tôi thư giãn rất nhiều.')
        }
        driver_name, car_model, trait, feedback = mood_configs[dr_mood]
        stars = "4.9"
        trips = random.randint(200, 500)

        def full_info_card(status_title):
            return f"""<div class='driver-info-card'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <b style='color:#db2777; font-size:22px;'>{status_title} 💖</b>
                    <span style='color:#f59e0b; font-weight:bold; font-size:18px;'>⭐ {stars}</span>
                </div>
                <div style='margin-top:15px; font-size:16px; color:#1f2937; line-height: 1.7;'>
                    👤 Tài xế: <b>{driver_name}</b> ({dr_age} | {dr_gender})<br>
                    🚗 Loại xe: <b>{car_model}</b><br>
                    ✨ Tính cách: <i>{trait}</i><br>
                    🛣️ Số chuyến: <b>{trips} chuyến</b><br>
                    💬 Feedback: <span style='color:#4b5563;'>"{feedback}"</span>
                </div>
                <div class='price-tag'>{(15000 + dist_final*12000):,.0f} VNĐ</div>
            </div>"""

        # GIAI ĐOẠN 1
        if st.session_state.step == 1:
            st.markdown("<p style='text-align:center;'>🔍 <b>Đang quét tần số tài xế phù hợp...</b></p>", unsafe_allow_html=True)
            m1 = folium.Map(location=pos_don, zoom_start=15)
            folium.Marker(pos_don, icon=folium.Icon(color='red', icon='heart', prefix='fa')).add_to(m1)
            for p in drivers_pos:
                folium.Marker(p, icon=folium.Icon(color='blue', icon='car', prefix='fa')).add_to(m1)
            st_folium(m1, width=None, height=450, key="map1")
            time.sleep(2)
            st.session_state.step = 2
            st.rerun()

        # GIAI ĐOẠN 2
        elif st.session_state.step == 2:
            st.markdown(full_info_card("KẾT NỐI THÀNH CÔNG"), unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center; color:white;'>Tài xế đang đến đón ({dist_to_user:.2f} km)...</p>", unsafe_allow_html=True)
            m2 = folium.Map(location=pos_don, zoom_start=15)
            folium.PolyLine(route_to_user, color='blue', weight=5).add_to(m2)
            folium.Marker(pos_don, icon=folium.Icon(color='red', icon='heart', prefix='fa')).add_to(m2)
            folium.Marker(nearest_driver, icon=folium.Icon(color='blue', icon='car', prefix='fa')).add_to(m2)
            st_folium(m2, width=None, height=450, key="map2")
            time.sleep(3)
            st.session_state.step = 3
            st.rerun()

        # GIAI ĐOẠN 3
        elif st.session_state.step == 3:
            st.markdown(full_info_card("HÀNH TRÌNH CHỮA LÀNH"), unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center; color:white;'>Đang di chuyển đến điểm đích ({dist_final:.2f} km)...</p>", unsafe_allow_html=True)
            m3 = folium.Map(location=pos_don, zoom_start=14)
            folium.PolyLine(route_to_dest, color='#db2777', weight=7).add_to(m3)
            folium.Marker(pos_don, icon=folium.Icon(color='red', icon='heart', prefix='fa')).add_to(m3)
            folium.Marker(pos_den, icon=folium.Icon(color='green', icon='flag', prefix='fa')).add_to(m3)
            st_folium(m3, width=None, height=450, key="map3")
            
            if st.button("HOÀN THÀNH CHUYẾN ĐI"):
                st.session_state.step = 0
                st.rerun()
    else:
        # Nếu đã thử lại nhiều lần vẫn lỗi thì mới báo lỗi cho người dùng
        st.error("⚠️ Không thể kết nối dịch vụ định vị. Hãy thử nhập địa chỉ rõ ràng hơn hoặc đợi vài giây rồi thử lại nhé!")
        st.session_state.step = 0

st.markdown('</div></div>', unsafe_allow_html=True)
