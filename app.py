import streamlit as st
import requests
import streamlit.components.v1 as components

# Cấu hình trang (phải đặt ở dòng đầu tiên)
st.set_page_config(page_title="Hệ Thống Học Tập AI & Diễn Đàn", page_icon="🔒", layout="wide")

# 🔴 LINK APPS SCRIPT CỦA BRO:
GSHEETS_URL = "https://script.google.com/macros/s/AKfycbzV0KqHng6Edeb8LupXLSY84M_v4VnenGHenVWj_d7pvzVlsq2KWwh7dN-xwOSP33oh/exec"

# Khởi tạo bộ nhớ tạm (Session State) để lưu trạng thái đăng nhập
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["fullname"] = ""

# Hàm gửi dữ liệu lên Google Sheets (giữ nguyên bản chuẩn của bro)
def send_request(payload):
    try:
        res = requests.post(GSHEETS_URL, json=payload, timeout=10)
        try:
            return res.json()
        except Exception:
            st.error("🚨 LỖI TỪ GOOGLE: CSDL không trả về JSON. Nội dung thực tế là:")
            st.code(res.text[:500])
            return None
    except Exception as e:
        st.error(f"Lỗi kết nối máy chủ: {e}")
        return None

# ==========================================
# KHU VỰC 1: CHẶN CỬA - ĐĂNG NHẬP / ĐĂNG KÝ VỚI GOOGLE SHEETS
# ==========================================
if not st.session_state["logged_in"]:
    st.title("🔒 Cổng Đăng Nhập Hệ Thống")
    st.markdown("Vui lòng đăng nhập hoặc đăng ký tài khoản để truy cập vào trợ lý AI và Diễn Đàn.")
    
    tab1, tab2 = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký tài khoản"])
    
    # --- TAB ĐĂNG NHẬP ---
    with tab1:
        st.subheader("Đăng nhập hệ thống")
        log_user = st.text_input("Tên đăng nhập (Username)", key="log_user")
        log_pass = st.text_input("Mật khẩu", type="password", key="log_pass")
        
        if st.button("🚀 Đăng nhập", type="primary", use_container_width=True):
            if not log_user or not log_pass:
                st.warning("Vui lòng nhập đủ thông tin!")
            else:
                with st.spinner("Đang kiểm tra thông tin với máy chủ..."):
                    res = send_request({"action": "login", "username": log_user.strip(), "password": log_pass})
                    if res:
                        if res.get("status") == "success":
                            # Lưu thông tin thật từ Google Sheets vào Session State
                            st.session_state["logged_in"] = True
                            st.session_state["username"] = log_user.strip()
                            st.session_state["fullname"] = res.get("fullname", log_user)
                            st.success(res.get("message"))
                            st.rerun() # Tải lại trang để mở khóa bên trong
                        else:
                            st.error(res.get("message"))
                            
    # --- TAB ĐĂNG KÝ ---
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
                with st.spinner("Đang lưu tài khoản lên Google Sheets..."):
                    # Gửi yêu cầu đăng ký thật lên Google Sheets
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

# ==========================================
# KHU VỰC 2: BÊN TRONG (ĐÃ ĐĂNG NHẬP THÀNH CÔNG)
# ==========================================
else:
    # Thanh Sidebar chào mừng và nút đăng xuất
    with st.sidebar:
        st.write(f"🎉 Xin chào, **{st.session_state['fullname']}**!")
        st.info("Băng thông hệ thống đã mở khóa.")
        
        if st.button("🚪 Đăng xuất", use_container_width=True):
            # Xóa sạch thông tin phiên đăng nhập
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.session_state["fullname"] = ""
            st.rerun() # Văng về màn hình đăng nhập
            
        st.markdown("---")
        st.markdown("### 🧭 Điều hướng")
        st.page_link("pages/1_Dien_Dan.py", label="💬 Vào Diễn Đàn ngay", icon="👉")

    # Giao diện chính bên trong (Hiển thị Botpress AI của bro)
    st.title("🤖 Trợ Giúp AI & Không Gian Học Tập")
    st.success(f"Chào mừng **{st.session_state['fullname']}** đã đăng nhập vào hệ thống thành công!")
    
    st.markdown("---")
    st.subheader("💬 Trò chuyện trực tiếp với Trợ lý AI:")

    # Nhúng mã Botpress của bro vào đây
    botpress_code = """
    <div style="height: 600px; width: 100%; position: relative;">
        <script src="https://cdn.botpress.cloud/webchat/v5.0/inject.js"></script>
        <script src="https://files.bpcontent.cloud/2026/08/01/04/20260801041109-K5GAT84Z.js" defer></script>
    </div>
    """
    
    # Hiển thị khung chat Botpress lên Streamlit
    components.html(botpress_code, height=650, scrolling=True)
