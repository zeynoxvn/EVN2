import streamlit as st
# Đặt đoạn này ở đầu các file trang con trong thư mục pages/
if not st.session_state.get("logged_in", False):
    st.error("⚠️ Bạn chưa đăng nhập! Vui lòng quay lại trang chính để đăng nhập trước khi sử dụng tính năng này.")
    st.page_link("app.py", label="🔑 Quay lại Trang chủ để Đăng nhập", icon="👉")
    st.stop() # Dừng không cho chạy tiếp nội dung bên dưới
st.title("🏆 Bảng Xếp Hạng đang được xây dựng!")
