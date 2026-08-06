import streamlit as st
import streamlit as st
import requests

# ... (Giữ nguyên toàn bộ phần code còn lại của bro từ đoạn này trở xuống) ...
import requests
import streamlit.components.v1 as components

# Cấu hình trang
st.set_page_config(page_title="EVN by AN,DŨNG - Cổng Học Tập", page_icon="⚡", layout="wide")

# --- CSS GIAO DIỆN XANH - TRẮNG HIỆN ĐẠI (PHONG CÁCH CANVA) ---
st.markdown("""
    <style>
    .stApp { background-color: #F4F6F9; }
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        background: #1E88E5;
        color: white;
        border: none;
    }
    .stButton > button:hover { background: #1565C0; color: white; }
    </style>
""", unsafe_allow_html=True)

# 🔴 LINK APPS SCRIPT CỦA BRO:
GSHEETS_URL = "https://script.google.com/macros/s/AKfycbzV0KqHng6Edeb8LupXLSY84M_v4VnenGHenVWj_d7pvzVlsq2KWwh7dN-xwOSP33oh/exec"

# Khởi tạo bộ nhớ tạm an toàn
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "fullname" not in st.session_state:
    st.session_state["fullname"] = ""

def send_request(payload):
    try:
        res = requests.post(GSHEETS_URL, json=payload, timeout=10)
        return res.json()
    except Exception as e:
        st.error(f"Lỗi kết nối máy chủ: {e}")
        return None

# ==========================================
# 1. MÀN HÌNH ĐĂNG NHẬP / ĐĂNG KÝ
# ==========================================
if not st.session_state["logged_in"]:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h2 style='text-align: center; color: #1E88E5;'>⚡ EVN by AN,DŨNG</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666;'>Đăng nhập để trải nghiệm không gian học tập thông minh.</p>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký"])
        
        with tab1:
            log_user = st.text_input("Tên đăng nhập", key="log_user")
            log_pass = st.text_input("Mật khẩu", type="password", key="log_pass")
            if st.button("🚀 Đăng nhập ngay", use_container_width=True):
                if not log_user or not log_pass:
                    st.warning("Vui lòng điền đủ thông tin!")
                else:
                    res = send_request({"action": "login", "username": log_user.strip(), "password": log_pass})
                    if res and res.get("status") == "success":
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = log_user.strip()
                        st.session_state["fullname"] = res.get("fullname", log_user)
                        st.success("Đăng nhập thành công!")
                        st.rerun()
                    else:
                        st.error(res.get("message", "Sai tài khoản hoặc mật khẩu!"))
                        
        with tab2:
            reg_user = st.text_input("Tên đăng nhập (không dấu)", key="reg_user")
            reg_name = st.text_input("Họ và tên thật", key="reg_name")
            reg_pass = st.text_input("Mật khẩu", type="password", key="reg_pass")
            reg_pass2 = st.text_input("Nhập lại mật khẩu", type="password", key="reg_pass2")
            if st.button("✨ Tạo tài khoản", use_container_width=True):
                if not reg_user or not reg_name or not reg_pass:
                    st.warning("Vui lòng điền đủ thông tin!")
                elif reg_pass != reg_pass2:
                    st.error("Mật khẩu không khớp!")
                else:
                    res = send_request({"action": "register", "username": reg_user.strip(), "password": reg_pass, "fullname": reg_name.strip()})
                    if res and res.get("status") == "success":
                        st.success("Đăng ký thành công! Hãy chuyển sang tab Đăng nhập.")
                    else:
                        st.error(res.get("message", "Lỗi đăng ký!"))

# ==========================================
# 2. GIAO DIỆN BÊN TRONG KHI ĐÃ ĐĂNG NHẬP
# ==========================================
else:
    current_fullname = st.session_state.get('fullname', 'Thành viên')
    
    # Sidebar điều hướng gọn gàng, có đủ Bảng Xếp Hạng và Trắc Nghiệm AI
  # Sidebar điều hướng
   # Sidebar điều hướng
    with st.sidebar:
        st.markdown(f"### 👋 Chào, **{current_fullname}**")
        st.info("Trạng thái: Hoạt động 🟢")
        st.markdown("---")
        st.markdown("### 🧭 Menu Điều Hướng")
        st.page_link("app.py", label="🏠 Trang Chủ (AI Chat)", icon="⚡")
        st.page_link("pages/1_Dien_Dan.py", label="💬 Diễn Đàn Thảo Luận", icon="🗣️")
        st.page_link("pages/2_Bang_Xep_Hang.py", label="🏆 Bảng Xếp Hạng", icon="📊")
       # st.page_link("pages/3_Trac_Nghiem_AI.py", label="📝 Trắc Nghiệm AI", icon="🤖")
        st.page_link("pages/4_Gop_Y.py", label="📮 Hòm Thư Góp Ý", icon="📥")
        st.page_link("pages/5_Ket_Ban.py", label="👥 Quản Lý Kết Ban", icon="🤝")
        st.page_link("pages/4_Kiem_Duyet_Admin.py", label="🛡️ Kiểm Duyệt Admin", icon="🔒")
        st.page_link("pages/7_San_Dau.py", label="⚔️ Vào Sàn Đấu Toán Học", icon="🔥")
        st.markdown("---")
        if st.button("🚪 Đăng xuất", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.session_state["fullname"] = ""
            st.rerun()
    # Nội dung Trang chủ (Chat AI)
    st.title("🤖 Trợ Giúp AI & Không Gian Học Tập")
    st.markdown(f"Chào mừng **{current_fullname}** đã đăng nhập thành công!")
    st.markdown("---")
    st.subheader("💬 Trò chuyện trực tiếp với Trợ lý AI:")

    botpress_code = """
    <div style="height: 600px; width: 100%; position: relative; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
        <script src="https://cdn.botpress.cloud/webchat/v5.0/inject.js"></script>
        <script src="https://files.bpcontent.cloud/2026/08/01/04/20260801041109-K5GAT84Z.js" defer></script>
    </div>
    """
    components.html(botpress_code, height=630, scrolling=True)
