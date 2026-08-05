import streamlit as st
import pandas as pd

st.set_page_config(page_title="EVN by AN,DŨNG", page_icon="⚡", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Hàm kiểm tra tài khoản từ Google Sheets (dạng file công khai link CSV)
def check_login(username_input, password_input):
    try:
        # THAY LINK DƯỚI BẰNG LINK GOOGLE SHEETS CỦA BRO (đã xuất bản dạng CSV hoặc public)
        # Hoặc dùng link Google Sheets dạng export format csv:
        # Ví dụ: sheet_url = "https://docs.google.com/spreadsheets/d/ID_CUA_SHEET/export?format=csv"
        sheet_url = "https://script.google.com/macros/s/AKfycbzV0KqHng6Edeb8LupXLSY84M_v4VnenGHenVWj_d7pvzVlsq2KWwh7dN-xwOSP33oh/exec" 
        df = pd.read_csv(sheet_url)
        
        # Giả sử trong Google Sheets của bro có cột tên là 'username' và 'password'
        user_match = df[(df['username'] == username_input) & (df['password'].astype(str) == str(password_input))]
        
        if not user_match.empty:
            return True
    except Exception as e:
        # Nếu chưa cấu hình link sheet, tạm thời cho phép pass để test hoặc báo lỗi
        st.warning(f"Chưa kết nối được Google Sheets: {e}")
    
    return False

# --- GIAO DIỆN ĐĂNG NHẬP ---
if not st.session_state.logged_in:
    st.title("⚡ EVN by AN,DŨNG - Đăng nhập hệ thống")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Tên đăng nhập")
        password = st.text_input("Mật khẩu", type="password")
        if st.button("Đăng nhập", use_container_width=True):
            # Kiểm tra với Google Sheets hoặc tài khoản dự phòng của bro
            if (username == "phanle" and password == "1902") or check_login(username, password):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Sai tên đăng nhập hoặc mật khẩu, hoặc chưa kết nối đúng Google Sheets!")

# --- SAU KHI ĐĂNG NHẬP THÀNH CÔNG (CÁC TRANG CHÍNH) ---
else:
    st.sidebar.title("⚡ EVN by AN,DŨNG")
    menu = st.sidebar.selectbox(
        "Chọn chức năng", 
        ["Trang chủ (Dashboard)", "Diễn đàn", "Hòm thư góp ý", "Bảng xếp hạng", "Kiểm duyệt Admin"]
    )
    
    st.sidebar.divider()
    if st.sidebar.button("Đăng xuất", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    if menu == "Trang chủ (Dashboard)":
        st.header("📊 Tổng quan hệ thống điện lực")
        col1, col2, col3 = st.columns(3)
        col1.metric("Tổng công suất tiêu thụ", "1,245 kW", "+4%")
        col2.metric("Số lượng trạm hoạt động", "42/42", "Ổn định")
        col3.metric("Yêu cầu cần xử lý", "12", "Cần chú ý")
        st.line_chart([10, 20, 15, 25, 30, 40, 35])

    elif menu == "Diễn đàn":
        st.header("💬 Diễn đàn nội bộ")
        st.text_input("🔍 Tìm kiếm bài viết...")

    elif menu == "Hòm thư góp ý":
        st.header("📥 Hòm thư góp ý & Khiếu nại")
        st.text_input("Tiêu đề góp ý")
        st.text_area("Nội dung chi tiết")

    elif menu == "Bảng xếp hạng":
        st.header("🏆 Bảng xếp hạng hiệu suất")
        df_ranking = pd.DataFrame({
            "Hạng": [1, 2, 3],
            "Đơn vị": ["Phòng QLVH", "Trạm 2", "Đội sửa chữa"],
            "Điểm": [98.5, 94.2, 90.1]
        })
        st.dataframe(df_ranking, use_container_width=True)

    elif menu == "Kiểm duyệt Admin":
        st.header("🛡️ Khu vực kiểm duyệt Admin")
        st.warning("Khu vực quản trị cấp cao.")
