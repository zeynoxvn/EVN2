import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang
st.set_page_config(page_title="Cổng Thông Tin Học Tập", page_icon="🎓", layout="wide")

st.title("🎓 Chào mừng đến với Cổng Thông Tin")
st.write("Sử dụng Menu bên trái để vào Diễn đàn hoặc Đăng nhập.")
st.markdown("---")
st.subheader("🤖 Trợ Lý AI (Nhấn vào biểu tượng chat ở góc dưới)")

# Mã Botpress gốc thuần khiết nhất - An toàn tuyệt đối
botpress_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.botpress.cloud/webchat/v1/inject.js"></script>
    <script src="https://mediafiles.botpress.cloud/32180f7e-9675-4570-91cb-fe856586b71f/webchat/config.js" defer></script>
</head>
<body style="margin: 0; padding: 0; height: 100vh;">
</body>
</html>
"""

# Khung HTML đủ cao để không che mất nút chat
components.html(botpress_code, height=700, scrolling=True)
