import streamlit as st
import os
from datetime import datetime

# Cấu hình trang
st.set_page_config(page_title="Hòm Thư Góp Ý", page_icon="📮", layout="centered")

# 1. Chặn cửa: Bắt buộc phải đăng nhập tài khoản hệ thống mới vào được trang này
if not st.session_state.get("logged_in", False):
    st.error("⚠️ Bạn chưa đăng nhập! Vui lòng quay lại trang chính để đăng nhập trước.")
    st.page_link("app.py", label="🔑 Quay lại Trang chủ để Đăng nhập", icon="👉")
    st.stop()

st.title("📮 Hòm Thư Góp Ý & Báo Lỗi")
st.markdown("Mọi ý kiến đóng góp của bạn sẽ được gửi trực tiếp và bảo mật với quản trị viên.")
st.divider()

# Tên file lưu trữ góp ý trên server
FILE_NAME = "danh_sach_gop_y.txt"

# ==========================================
# PHẦN 1: DÀNH CHO HỌC SINH / NGƯỜI DÙNG (GỬI GÓP Ý)
# ==========================================
with st.form("form_gop_y"):
    st.write(f"📝 Góp ý với tên: **{st.session_state.get('fullname', 'Người dùng')}**")
    
    noi_dung_gop_y = st.text_area(
        "Nhập nội dung góp ý hoặc báo lỗi:",
        placeholder="Ví dụ: Trang web chạy rất mượt, thầy/cô bổ sung thêm..."
    )
    
    submitted = st.form_submit_button("🚀 Gửi Góp Ý Ngay", type="primary", use_container_width=True)
    
    if submitted:
        if not noi_dung_gop_y.strip():
            st.warning("Vui lòng nhập nội dung trước khi gửi!")
        else:
            thoi_gian = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            nguoi_gui = st.session_state.get('fullname', 'Ẩn danh')
            
            # Định dạng nội dung lưu vào file
            dong_gop_y = f"[{thoi_gian}] Người gửi: {nguoi_gui}\nNội dung: {noi_dung_gop_y.strip()}\n" + "-"*40 + "\n"
            
            try:
                with open(FILE_NAME, "a", encoding="utf-8") as f:
                    f.write(dong_gop_y)
                st.success("🎉 Cảm ơn bạn! Góp ý của bạn đã được gửi thành công đến quản trị viên.")
            except Exception as e:
                st.error(f"Có lỗi xảy ra: {e}")

st.divider()

# ==========================================
# PHẦN 2: KHU VỰC BẢO MẬT DÀNH RIÊNG CHO QUẢN TRỊ VIÊN (CÓ MẬT KHẨU)
# ==========================================
with st.expander("🔒 Dành cho Quản trị viên (Xem hòm thư)"):
    # Đặt mật khẩu quản trị của bro ở đây (có thể thay đổi tùy ý)
    ADMIN_PASSWORD = "andung123"  # <--- BRO ĐỔI MẬT KHẨU TẠI ĐÂY NÈ
    
    input_pass = st.text_input("Nhập mật khẩu quản trị viên để xem góp ý:", type="password")
    
    if input_pass == ADMIN_PASSWORD:
        st.success("🔓 Đăng nhập quyền quản trị thành công!")
        
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                noi_dung_file = f.read()
                
            if noi_dung_file.strip():
                st.text_area("Hòm thư góp ý hiện tại:", value=noi_dung_file, height=350)
                
                if st.button("🗑️ Xóa sạch tất cả hòm thư"):
                    open(FILE_NAME, "w", encoding="utf-8").close()
                    st.success("Đã dọn sạch hòm thư!")
                    st.rerun()
            else:
                st.info("Hòm thư hiện đang trống, chưa có ai góp ý.")
        else:
            st.info("Chưa có file dữ liệu góp ý nào được tạo.")
            
    elif input_pass:
        st.error("❌ Sai mật khẩu quản trị viên!")

st.divider()
st.page_link("app.py", label="🏠 Quay về Trang chủ", icon="⬅️")
