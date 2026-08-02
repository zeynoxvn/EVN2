import streamlit as st
import requests
# Đặt đoạn này ở đầu các file trang con trong thư mục pages/
if not st.session_state.get("logged_in", False):
    st.error("⚠️ Bạn chưa đăng nhập! Vui lòng quay lại trang chính để đăng nhập trước khi sử dụng tính năng này.")
    st.page_link("app.py", label="🔑 Quay lại Trang chủ để Đăng nhập", icon="👉")
    st.stop() # Dừng không cho chạy tiếp nội dung bên dưới
# Cấu hình trang
st.set_page_config(page_title="Tài Khoản", page_icon="👤", layout="centered")

# 🔴 DÁN LINK APPS SCRIPT CỦA FEN VÀO ĐÂY:
GSHEETS_URL = "https://script.google.com/macros/s/AKfycbzV0KqHng6Edeb8LupXLSY84M_v4VnenGHenVWj_d7pvzVlsq2KWwh7dN-xwOSP33oh/exec"

st.title("👤 Quản lý Tài Khoản")
st.page_link("app.py", label="🏠 Quay về Trang Chủ", use_container_width=False)
st.divider()

# Khởi tạo bộ nhớ tạm (Session State) để web nhớ ai đang đăng nhập
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["fullname"] = ""

# Hàm gửi dữ liệu lên Google Sheets
# Hàm gửi dữ liệu lên Google Sheets (Đã nâng cấp để bắt lỗi)
def send_request(payload):
    try:
        res = requests.post(GSHEETS_URL, json=payload, timeout=10)
        # Thử ép sang JSON, nếu lỗi thì in thẳng nội dung Google trả về ra màn hình
        try:
            return res.json()
        except Exception:
            st.error("🚨 LỖI TỪ GOOGLE: CSDL không trả về JSON. Nội dung thực tế là:")
            st.code(res.text[:500]) # In ra 500 ký tự đầu tiên của lỗi
            return None
    except Exception as e:
        st.error(f"Lỗi kết nối máy chủ: {e}")
        return None

# NẾU CHƯA ĐĂNG NHẬP -> HIỆN FORM ĐĂNG NHẬP / ĐĂNG KÝ
if not st.session_state["logged_in"]:
    tab1, tab2 = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký tài khoản"])
    
    # ==========================
    # TAB ĐĂNG NHẬP
    # ==========================
    with tab1:
        st.subheader("Đăng nhập hệ thống")
        log_user = st.text_input("Tên đăng nhập (Username)", key="log_user")
        log_pass = st.text_input("Mật khẩu", type="password", key="log_pass")
        
        if st.button("🚀 Đăng nhập", type="primary", use_container_width=True):
            if not log_user or not log_pass:
                st.warning("Vui lòng nhập đủ thông tin!")
            else:
                with st.spinner("Đang kiểm tra thông tin..."):
                    res = send_request({"action": "login", "username": log_user.strip(), "password": log_pass})
                    if res:
                        if res.get("status") == "success":
                            # Lưu thông tin vào bộ nhớ
                            st.session_state["logged_in"] = True
                            st.session_state["username"] = log_user
                            st.session_state["fullname"] = res.get("fullname", log_user)
                            st.success(res.get("message"))
                            st.rerun() # F5 lại trang
                        else:
                            st.error(res.get("message"))
                            
    # ==========================
    # TAB ĐĂNG KÝ
    # ==========================
    with tab2:
        st.subheader("Tạo tài khoản mới")
        reg_user = st.text_input("Tên đăng nhập (Viết liền không dấu)", key="reg_user")
        reg_name = st.text_input("Họ và tên thật của bạn", key="reg_name")
        reg_pass = st.text_input("Mật khẩu", type="password", key="reg_pass")
        reg_pass2 = st.text_input("Nhập lại mật khẩu", type="password", key="reg_pass2")
        
        if st.button("✨ Đăng ký ngay", type="primary", use_container_width=True):
            if not reg_user or not reg_name or not reg_pass:
                st.warning("Vui lòng điền đầy đủ thông tin!")
            elif reg_pass != reg_pass2:
                st.error("Mật khẩu nhập lại không khớp!")
            elif " " in reg_user:
                st.error("Tên đăng nhập không được chứa khoảng trắng!")
            else:
                with st.spinner("Đang tạo tài khoản..."):
                    res = send_request({
                        "action": "register", 
                        "username": reg_user.strip(), 
                        "password": reg_pass, 
                        "fullname": reg_name.strip()
                    })
                    if res:
                        if res.get("status") == "success":
                            st.success(res.get("message") + " Bạn có thể chuyển sang tab Đăng nhập để vào hệ thống.")
                        else:
                            st.error(res.get("message"))

# NẾU ĐÃ ĐĂNG NHẬP -> HIỆN LỜI CHÀO & NÚT ĐĂNG XUẤT
else:
    st.success(f"🎉 Xin chào, **{st.session_state['fullname']}**! Bạn đã đăng nhập thành công.")
    st.info("Bây giờ bạn có thể vào Diễn đàn để đăng bài và bình luận bằng tên thật của mình.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.page_link("pages/1_Dien_Dan.py", label="💬 Vào Diễn Đàn ngay", icon="👉")
    with col2:
        if st.button("🚪 Đăng xuất", use_container_width=True):
            # Xóa bộ nhớ
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.session_state["fullname"] = ""
            st.rerun()
