import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import time

# --- PHẦN 1: GIỮ NGUYÊN TOÀN BỘ LOGIC CŨ CỦA HỒNG PHÚC ---
mood_configs = {
    'Cần tâm sự': {'driver': 'Trần Minh Anh', 'car': 'VinFast VF8', 'trait': 'Thấu cảm, ấm áp'},
    'Cần yên tĩnh': {'driver': 'Lê Quốc Bảo', 'car': 'Toyota Camry', 'trait': 'Lịch sự, điềm đạm'},
    'Đang rất vui': {'driver': 'Nguyễn Hoàng Nam', 'car': 'Mazda 6', 'trait': 'Năng động, hóm hỉnh'},
    'Căng thẳng': {'driver': 'Đặng Mỹ Hạnh', 'car': 'Honda Accord', 'trait': 'Nhẹ nhàng, tinh tế'}
}

# --- PHẦN 2: THIẾT LẬP GIAO DIỆN ---
st.set_page_config(page_title="Grab Healing 💖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #db2777; }
    .driver-card { background: white; padding: 25px; border-radius: 15px; color: black; margin: 10px 0; border-left: 8px solid #fb7185; }
    h1, p, label { color: white !important; }
    .stButton>button { width: 100%; border-radius: 20px; font-weight: bold; color: #db2777; height: 50px; }
    </style>
    """, unsafe_allow_html=True)

st.title("Grab Healing 💖")
st.write("Dự án của Nguyễn Nam Hồng Phúc")

# Nhập liệu
in_don = st.text_input("📍 Điểm đón", value="TP. Hồ Chí Minh")
in_den = st.text_input("📍 Điểm đến", value="Vũng Tàu")
dr_mood = st.selectbox("🧠 Tâm trạng của bạn", list(mood_configs.keys()))

# --- PHẦN 3: XỬ LÝ KHI NHẤN NÚT ---
if st.button("BẮT ĐẦU HÀNH TRÌNH"):
    # 1. Giữ nguyên logic đợi 5 giây
    with st.spinner('💖 Đang tìm kiếm tần số chữa lành phù hợp...'):
        time.sleep(5) 
    
    # 2. Lấy dữ liệu từ Dictionary (Đảm bảo không mất thông tin)
    driver_data = mood_configs[dr_mood]
    ten_tai_xe = driver_data['driver']
    loai_xe = driver_data['car']
    tinh_cach = driver_data['trait']
    gia_tien = random.randint(100, 300) * 1000  # Giả lập giá tiền từ logic cũ

    # 3. Hiển thị Card thông tin (Đã fix lỗi sát khung)
    st.markdown(f"""
        <div class="driver-card">
            <h3 style="color: #be185d;">KẾT NỐI THÀNH CÔNG 💖</h3>
            <p style="color: #374151;">👤 Tài xế: <b>{ten_tai_xe}</b></p>
            <p style="color: #374151;">🚗 Xe: <b>{loai_xe}</b></p>
            <p style="color: #374151;">✨ Đặc điểm: <i>{tinh_cach}</i></p>
            <hr>
            <h2 style="color: #be185d; text-align: right;">{gia_tien:,} VNĐ</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # 4. Hiển thị bản đồ (Giữ nguyên Marker Trái tim và Lá cờ)
    # Tọa độ giả lập dựa trên trung tâm HCM, bạn có thể thay bằng hàm geocode của bạn nếu có
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

    # Vẽ đường nối (Path)
    folium.PolyLine([[10.7626, 106.6602], [10.7826, 106.6802]], color="#db2777", weight=5).add_to(m1)
    
    # Lệnh hiển thị map quan trọng nhất trên Streamlit
    st_folium(m1, width=700, height=450)
