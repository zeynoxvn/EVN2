import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang
st.set_page_config(page_title="Cổng Thông Tin Học Tập", page_icon="🎓", layout="wide")

st.title("🎓 Chào mừng đến với Cổng Thông Tin")
st.write("Sử dụng Menu bên trái để vào Diễn đàn hoặc Đăng nhập.")
st.markdown("---")
st.subheader("🤖 Trợ Lý AI Học Tập")

# Đoạn mã nhúng Botpress v5.0 (Cập nhật theo script mới của bạn)
botpress_code = """
<div style="height: 600px; width: 100%; position: relative;">
    <script src="https://cdn.botpress.cloud/webchat/v5.0/inject.js"></script>
    <script src="https://files.bpcontent.cloud/2026/08/01/04/20260801041109-K5GAT84Z.js" defer></script>
</div>
"""

# Nhúng khung chat vào Streamlit
components.html(botpress_code, height=650, scrolling=True)
