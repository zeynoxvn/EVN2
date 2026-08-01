import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang
st.set_page_config(page_title="Cổng Thông Tin Học Tập", page_icon="🎓", layout="wide")

st.title("🎓 Chào mừng đến với Cổng Thông Tin")
st.write("Sử dụng Menu bên trái để vào Diễn đàn hoặc Đăng nhập.")
st.markdown("---")
st.subheader("🤖 Trợ Lý AI Học Tập")

# Mã Botpress đã được ép tự động mở mà KHÔNG bị xoay vòng
botpress_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.botpress.cloud/webchat/v1/inject.js"></script>
    <script src="https://mediafiles.botpress.cloud/32180f7e-9675-4570-91cb-fe856586b71f/webchat/config.js" defer></script>
</head>
<body style="margin: 0; padding: 0; height: 100vh; overflow: hidden;">
    <script>
        // Lắng nghe Botpress, hễ nó tải xong cấu hình là bung lụa luôn khỏi cần nút
        window.addEventListener('message', function(event) {
            if (event.data && event.data.type === 'LIFECYCLE.LOADED') {
                window.botpressWebChat.sendEvent({ type: 'show' });
            }
        });
    </script>
</body>
</html>
"""

# Khung HTML hiển thị - tắt scrolling để không bị che khuất
components.html(botpress_code, height=650, scrolling=False)
