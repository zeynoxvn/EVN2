import streamlit as st
import pandas as pd

# Cấu hình trang web
st.set_page_config(page_title="EVN by AN,DŨNG", page_icon="⚡", layout="wide")

# Khởi tạo trạng thái đăng nhập
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- BƯỚC 1: XỬ LÝ GIAO DIỆN ĐĂNG NHẬP ---
if not st.session_state.logged_in:
    st.title("⚡ EVN by AN,DŨNG - Đăng nhập hệ thống")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Tên đăng nhập")
        password = st.text_input("Mật khẩu", type="password")
        if st.button("Đăng nhập", use_container_width=True):
            # Tài khoản mẫu: admin / 123456 (bro có thể đổi tùy ý)
            if username == "admin" and password == "123456":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Sai tên đăng nhập hoặc mật khẩu!")

# --- BƯỚC 2: SAU KHI ĐĂNG NHẬP THÀNH CÔNG (HIỂN THỊ CÁC TRANG) ---
else:
    # Thanh điều hướng bên trái (Sidebar)
    st.sidebar.title("⚡ EVN by AN,DŨNG")
    menu = st.sidebar.selectbox(
        "Chọn chức năng", 
        ["Trang chủ (Dashboard)", "Diễn đàn", "Hòm thư góp ý", "Bảng xếp hạng", "Kiểm duyệt Admin"]
    )
    
    st.sidebar.divider()
    if st.sidebar.button("Đăng xuất", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # 1. TRANG CHỦ
    if menu == "Trang chủ (Dashboard)":
        st.header("📊 Tổng quan hệ thống điện lực")
        col1, col2, col3 = st.columns(3)
        col1.metric("Tổng công suất tiêu thụ", "1,245 kW", "+4% so với hôm qua")
        col2.metric("Số lượng trạm hoạt động", "42/42", "Ổn định")
        col3.metric("Yêu cầu cần xử lý", "12", "Cần chú ý")
        
        st.subheader("Biểu đồ tiêu thụ điện năng")
        chart_data = [10, 20, 15, 25, 30, 40, 35]
        st.line_chart(chart_data)

    # 2. DIỄN ĐÀN
    elif menu == "Diễn đàn":
        st.header("💬 Diễn đàn nội bộ")
        st.text_input("🔍 Tìm kiếm bài viết...")
        if st.button("➕ Tạo bài viết mới"):
            st.success("Mở form tạo bài viết!")
        st.info("Chưa có bài viết nào được đăng gần đây.")

    # 3. HÒM THƯ GÓP Ý
    elif menu == "Hòm thư góp ý":
        st.header("📥 Hòm thư góp ý & Khiếu nại")
        st.text_input("Tiêu đề góp ý")
        st.text_area("Nội dung chi tiết")
        if st.button("Gửi góp ý"):
            st.success("Gửi thành công! Cảm ơn đóng góp của bạn.")

    # 4. BẢNG XẾP HẠNG
    elif menu == "Bảng xếp hạng":
        st.header("🏆 Bảng xếp hạng hiệu suất tiết kiệm điện")
        df = pd.DataFrame({
            "Hạng": [1, 2, 3],
            "Đơn vị / Phòng ban": ["Phòng Quản lý vận hành", "Trạm biến áp số 2", "Đội sửa chữa lưu động"],
            "Điểm hiệu suất": [98.5, 94.2, 90.1],
            "Trạng thái": ["Xuất sắc", "Tốt", "Khá"]
        })
        st.dataframe(df, use_container_width=True)

    # 5. KIỂM DUYỆT ADMIN
    elif menu == "Kiểm duyệt Admin":
        st.header("🛡️ Khu vực kiểm duyệt dành cho Admin")
        st.warning("Cảnh báo: Khu vực giới hạn quyền quản trị.")
        st.checkbox("Cho phép thành viên đăng bài tự do không cần kiểm duyệt")
        if st.button("Xóa bộ nhớ đệm hệ thống"):
            st.success("Đã làm sạch Cache!")
