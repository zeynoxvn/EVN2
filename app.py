import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang (Nhớ bật layout wide)
st.set_page_config(page_title="Cổng Thông Tin THCS", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

# --- BÙA CSS NÂNG CẤP GIAO DIỆN ---
custom_css = """
<style>
    /* Chỉnh phông chữ tổng thể và màu nền */
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@600;800&family=Inter:wght@400;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Thiết kế lại Tiêu đề chính với dải màu Gradient */
    .hero-title {
        font-family: 'Nunito', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #4F46E5, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    
    /* Căn lề và tạo style thẻ (Card) cho các khu vực */
    .stMarkdown { margin-bottom: 15px; }
    
    .info-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border-left: 5px solid #10B981;
    }
    
    /* Tùy chỉnh Menu Sidebar cho thân thiện hơn */
    [data-testid="stSidebar"] {
        background-color: #F1F5F9;
        border-right: 1px solid #E2E8F0;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- ÁP DỤNG GIAO DIỆN VÀO NỘI DUNG ---

# Tiêu đề siêu xịn
st.markdown('<h1 class="hero-title">🎓 Cổng Thông Tin Học Tập</h1>', unsafe_allow_html=True)

# Lời chào trong khối thẻ (Card)
st.markdown("""
<div class="info-card">
    <h3 style="margin-top:0px; font-family:'Nunito'; color:#1E293B;">👋 Xin chào các bạn học sinh!</h3>
    <p style="color:#475569; font-size: 16px;">Chào mừng đến với không gian học tập tích cực. Hãy sử dụng Menu bên trái để khám phá, hoặc lướt xuống để trò chuyện với Trợ lý AI nhé!</p>
</div>
""", unsafe_allow_html=True)

st.divider() # Đường kẻ mờ phân cách

# --- KHU VỰC TRỢ LÝ AI (CODE NHƯ CŨ) ---
st.subheader("🤖 Khu Vực Trợ Lý AI")

import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang
st.set_page_config(page_title="Cổng Thông Tin Học Tập", page_icon="🎓", layout="wide")

st.title("🎓 Chào mừng đến với Cổng Thông Tin")
st.write("Sử dụng Menu bên trái để vào Diễn đàn hoặc Đăng nhập.")
st.markdown("---")
st.subheader("🤖 Trợ Lý AI (Nhìn xuống góc dưới bên phải)")

# Code nhúng Botpress (Chỉ cần dán 2 dòng script của fen vào phần head)
botpress_code = """
<!DOCTYPE html>
<html>
<head>
    <!-- DÁN 2 DÒNG SCRIPT CỦA BOTPRESS VÀO ĐÂY -->
    <script src="https://cdn.botpress.cloud/webchat/v1/inject.js"></script>
    <script src="https://mediafiles.botpress.cloud/MÃ_CỦA_FEN_LẤY_TRÊN_TRANG_CHỦ/webchat/config.js" defer></script>
</head>
<body style="margin: 0; padding: 0;">
</body>
</html>
"""

# Khởi tạo khung HTML
components.html(botpress_code, height=600)
botpress_code = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.botpress.cloud/webchat/v1/inject.js"></script>
    <script src="https://mediafiles.botpress.cloud/32180f7e-9675-4570-91cb-fe856586b71f/webchat/config.js" defer></script>
</head>
<body style="margin: 0; padding: 0; height: 100vh;">
    <script>
        // Bùa ép cửa sổ chat tự động bung ra khi load xong
        window.addEventListener('message', function(event) {
            if (event.data && event.data.type === 'LIFECYCLE.LOADED') {
                window.botpressWebChat.sendEvent({ type: 'show' });
            }
        });
    </script>
</body>
</html>
"""
