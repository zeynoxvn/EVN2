import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang
st.set_page_config(page_title="Cổng Thông Tin Học Tập", page_icon="🎓", layout="wide")

st.title("🎓 Chào mừng đến với Cổng Thông Tin")
st.write("Sử dụng Menu bên trái để vào Diễn đàn hoặc Đăng nhập.")
st.markdown("---")
st.subheader("🤖 Trợ Lý AI (Khu vực Chatbot)")

# Mã Botpress đã được tối ưu và cưỡng chế mở
botpress_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.botpress.cloud/webchat/v1/inject.js"></script>
</head>
<body style="margin: 0; padding: 0; overflow: hidden;">
    <script>
        // Khởi tạo trực tiếp bằng ID của bro
        window.botpressWebChat.init({
            "clientId": "32180f7e-9675-4570-91cb-fe856586b71f",
            "hostUrl": "https://cdn.botpress.cloud/webchat/v1",
            "messagingUrl": "https://messaging.botpress.cloud",
            "botName": "Trợ lý Học tập",
            "theme": "prism",
            "themeColor": "#2563eb"
        });
        
        // Bùa ép mở khung chat tự động 100%
        window.botpressWebChat.onEvent(
            function (event) {
                if (event.type === 'LIFECYCLE.LOADED') {
                    window.botpressWebChat.sendEvent({ type: 'show' });
                }
            },
            ['LIFECYCLE.LOADED']
        );
    </script>
</body>
</html>
"""

# Khởi tạo khung HTML để hiển thị chatbot
components.html(botpress_code, height=650, scrolling=True)
