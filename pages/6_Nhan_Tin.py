import streamlit as st
import requests
from datetime import datetime

# --- DÁN LINK API WEB APP URL CỦA BRO VÀO ĐÂY ---
API_URL = "https://script.google.com/macros/s/AKfycbzV0KqHng6Edeb8LupXLSY84M_v4VnenGHenVWj_d7pvzVlsq2KWwh7dN-xwOSP33oh/exec" 

if "chat_with" not in st.session_state:
    st.warning("Vui lòng chọn một người bạn để bắt đầu trò chuyện.")
    st.page_link("pages/5_Ket_Ban.py", label="Quay lại", icon="⬅️")
    st.stop()

friend_name = st.session_state.chat_with
# Giả sử bro đang lưu tên đăng nhập trong st.session_state.username
current_user = st.session_state.get("username", "Tài khoản của tôi") 

if st.button("⬅️ Quay lại trang Kết bạn"):
    st.switch_page("pages/5_Ket_Ban.py")

st.title(f"💬 Trò chuyện với {friend_name}")
st.divider()

# --- 1. LẤY LỊCH SỬ TIN NHẮN TỪ APP SCRIPT ---
# Gọi action = "get_messages"
payload_get = {
    "action": "get_messages",
    "user1": current_user,
    "user2": friend_name
}

try:
    response = requests.post(API_URL, json=payload_get)
    data = response.json()
    chat_history = data.get("messages", [])
except Exception as e:
    st.error("Không thể tải tin nhắn!")
    chat_history = []

# --- 2. HIỂN THỊ TIN NHẮN ---
for msg in chat_history:
    role = "user" if msg["sender"] == current_user else "assistant"
    with st.chat_message(role):
        st.write(msg["content"])
        # Nếu thích bro có thể in cả timestamp ra cho giống thật
        # st.caption(f"🕒 {msg['timestamp']}")

# --- 3. Ô NHẬP TIN NHẮN MỚI ---
if prompt := st.chat_input(f"Nhắn tin cho {friend_name}..."):
    
    # Hiển thị ngay lên màn hình
    with st.chat_message("user"):
        st.write(prompt)
    
    # Lấy giờ hiện tại
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Gọi action = "send_message"
    payload_send = {
        "action": "send_message",
        "sender": current_user,
        "receiver": friend_name,
        "content": prompt,
        "timestamp": now
    }
    
    # Bắn request lên Google Sheets
    requests.post(API_URL, json=payload_send)
    
    # Tải lại trang để chat update
    st.rerun()
