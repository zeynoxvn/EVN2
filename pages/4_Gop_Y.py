import streamlit as st
# Chặn cửa: Bắt buộc phải đăng nhập mới được vào trang này
if not st.session_state.get("logged_in", False):
    st.error("⚠️ Bạn chưa đăng nhập! Vui lòng quay lại trang chính để đăng nhập trước.")
    st.page_link("app.py", label="🔑 Quay lại Trang chủ để Đăng nhập", icon="👉")
    st.stop()
import os
from datetime import datetime

# Cấu hình trang
st.set_page_config(page_title="Hòm Thư Góp Ý", page_icon="📮", layout="centered")

# Kiểm tra đăng nhập
if not st.session_state.get("logged_in", False):
    st.error("⚠️ Bạn chưa đăng nhập! Vui lòng quay lại trang chính để đăng nhập trước.")
    st.page_link("app.py", label="🔑 Quay lại Trang chủ để Đăng nhập", icon="👉")
    st.stop()

st.title("📮 Hòm Thư Góp Ý & Báo Lỗi")
st.markdown("Mọi ý kiến đóng góp của bạn sẽ được lưu trực tiếp vào hệ thống để quản trị viên theo dõi.")
st.divider()

# Tên file lưu trữ trên server
FILE_NAME = "danh_sach_gop_y.txt"

# Form nhập góp ý
with st.form("form_gop_y"):
    st.write(f"📝 Góp ý với tên: **{st.session_state.get('fullname', 'Người dùng')}**")
    
    noi_dung_gop_y = st.text_area(
        "Nhập nội dung góp ý hoặc báo lỗi:",
        placeholder="Ví dụ: Trang web chạy rất mượt..."
    )
    
    submitted = st.form_submit_button("🚀 Gửi Góp Ý Ngay", type="primary", use_container_width=True)
    
    if submitted:
        if not noi_dung_gop_y.strip():
            st.warning("Vui lòng nhập nội dung trước khi gửi!")
        else:
            # Lấy thời gian hiện tại
            thoi_gian = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            nguoi_gui = st.session_state.get('fullname', 'Ẩn danh')
            
            # Định dạng nội dung lưu
            dong_gop_y = f"[{th_oi_gian if 'th_oi_gian' in locals() else thoi_gian}] {nguoi_gui}: {noi_dung_gop_y.strip()}\n" + "-"*40 + "\n"
            
            # Ghi vào file text
            try:
                with open(FILE_NAME, "a", encoding="utf-8") as f:
                    f.write(dong_gop_y)
                st.success("🎉 Cảm ơn bạn! Góp ý của bạn đã được gửi thành công.")
            except Exception as e:
                st.error(f"Có lỗi khi lưu file: {e}")

st.divider()

# (Tùy chọn) Khu vực hiển thị danh sách góp ý để bro đọc trực tiếp trên web (chỉ tài khoản của bro thấy hoặc hiện chung)
if os.path.exists(FILE_NAME):
    with st.expander("📂 Xem lại các góp ý đã nhận (Dành cho quản trị viên)"):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            noi_dung_file = f.read()
        if noi_dung_file.strip():
            st.text_area("Hộp thư:", value=noi_dung_file, height=300)
            if st.button("🗑️ Xóa sạch hòm thư"):
                open(FILE_NAME, "w", encoding="utf-8").close()
                st.rerun()
        else:
            st.info("Hòm thư hiện đang trống.")

st.page_link("app.py", label="🏠 Quay về Trang chủ", icon="⬅️")
