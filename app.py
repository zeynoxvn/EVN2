import streamlit as st

# Cấu hình giao diện Trang chủ
st.set_page_config(page_title="Cổng Thông Tin Học Tập", page_icon="🏫", layout="centered")

st.title("🎓 Cổng Thông Tin & Diễn Đàn Học Tập THCS")

st.write("Chào mừng bạn đến với hệ thống hỗ trợ học tập trực tuyến tích hợp AI!")

st.divider()

st.subheader("📌 Vui lòng chọn tính năng:")

# Các nút dẫn vào các trang chức năng
st.page_link("pages/0_Tai_Khoan.py", label="👤 Đăng Nhập / Đăng Ký", use_container_width=True)
st.page_link("pages/1_Dien_Dan.py", label="💬 Vào Diễn Đàn Thảo Luận", use_container_width=True)

# 2 nút này tạm ẩn vì bro chưa làm, chừng nào làm thì xóa dấu # đi nhé
# st.page_link("pages/2_Bang_Xep_Hang.py", label="🏆 Xem Bảng Xếp Hạng", use_container_width=True)
# st.page_link("pages/3_Trac_Nghiem_AI.py", label="📝 Làm Trắc Nghiệm", use_container_width=True)

st.page_link("pages/4_Kiem_Duyet_Admin.py", label="🛡️ Quản Trị Hệ Thống (Admin)", use_container_width=True)
