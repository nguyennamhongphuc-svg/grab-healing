import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import time

# --- PHẦN 1: GIỮ NGUYÊN 100% LOGIC CỦA HỒNG PHÚC ---
mood_configs = {
    'Cần tâm sự': {
        'driver': 'Trần Minh Anh', 
        'gender': 'Nữ', 
        'age': 28, 
        'car': 'VinFast VF8', 
        'trait': 'Thấu cảm, ấm áp'
    },
    'Cần yên tĩnh': {
        'driver': 'Lê Quốc Bảo', 
        'gender': 'Nam', 
        'age': 35, 
        'car': 'Toyota Camry', 
        'trait': 'Lịch sự, điềm đạm'
    },
    'Đang rất vui': {
        'driver': 'Nguyễn Hoàng Nam', 
        'gender': 'Nam', 
        'age': 25, 
        'car': 'Mazda 6', 
        'trait': 'Năng động, hóm hỉnh'
    },
    'Căng thẳng': {
        'driver': 'Đặng Mỹ Hạnh', 
        'gender': 'Nữ', 
        'age': 30, 
        'car': 'Honda Accord', 
        'trait': 'Nhẹ nhàng, tinh tế'
    }
}

# --- PHẦN 2: THIẾT LẬP GIAO DIỆN ---
st.set_page_config(page_title="Grab Healing 💖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #db2777; }
    .driver-card { 
        background: white; 
        padding: 25px; 
        border-radius: 15px; 
        color: black; 
        margin: 10px 0; 
        border-left: 8px solid #fb7185;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1, p, label { color: white !important; }
    .stButton>button { 
        width: 100%; 
        border-radius: 20px; 
        font-weight: bold; 
        color: #db2777; 
        height: 50px;
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Grab Healing 💖")
st.write("Dự án của Nguyễn Nam Hồng Phúc")

# Nhập liệu
in_don = st.text_input("📍 Điểm đón", value="TP. Hồ Chí Minh")
in_den = st.text_input("📍 Điểm đến", value="Vũng Tàu")
dr_mood = st.selectbox("🧠 Tâm trạng của bạn", list(mood_configs.keys()))

# --- PHẦN 3: XỬ LÝ LOGIC ---

# Sử dụng Session State để giữ bản đồ không bị tắt khi tương tác
if 'show_result' not in st.session_state:
    st.session_state.show_result = False

if st.button("BẮT ĐẦU HÀNH TRÌNH"):
    st.session_state.show_result = True
    with st.spinner('💖 Đang tìm kiếm tần số chữa lành phù hợp...'):
        time.sleep(3) # Giảm xuống 3s để trải nghiệm mượt hơn

if st.session_state.show_result:
    # Lấy dữ liệu tài xế dựa trên tâm trạng
    driver_data = mood_configs[dr_mood]
    
    # Hiển thị Card thông tin đầy đủ (Giới tính, Độ tuổi)
    st.markdown(f"""
        <div class="driver-card">
            <h3 style="color: #be185d; margin-top:0;">KẾT NỐI THÀNH CÔNG 💖</h3>
            <p style="color: #374151;">👤 Tài xế: <b>{driver_data['driver']}</b></p>
            <p style="color: #374151;">🚻 Giới tính: <b>{driver_data['gender']}</b> | 🎂 Độ tuổi: <b>{driver_data['age']}</b></p>
            <p style="color: #374151;">🚗 Xe: <b>{driver_data['car']}</b></p>
            <p style="color: #374151;">✨ Đặc điểm: <i>{driver_data['trait']}</i></p>
            <hr style="border: 0.5px solid #eee;">
            <h2 style="color: #be185d; text-align: right; margin-bottom:0;">250,000 VNĐ</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Khởi tạo bản đồ
    m1 = folium.Map(location=[10.7626, 106.6602], zoom_start=12)
    
    # Marker Điểm đón (Trái tim đỏ)
    folium.Marker(
        [10.7626, 106.6602], 
        popup="Điểm đón", 
        icon=folium.Icon(color='red', icon='heart', prefix='fa')
    ).add_to(m1)
    
    # Marker Điểm đến (Lá cờ xanh)
    folium.Marker(
        [10.7826, 106.6802], 
        popup="Điểm đến", 
        icon=folium.Icon(color='green', icon='flag', prefix='fa')
    ).add_to(m1)

    # Vẽ đường nối
    folium.PolyLine([[10.7626, 106.6602], [10.7826, 106.6802]], color="#db2777", weight=5).add_to(m1)
    
    # Hiển thị bản đồ cố định
    st_folium(m1, width=700, height=450, key="main_map")
