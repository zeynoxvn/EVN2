import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang
st.set_page_config(page_title="Cổng Thông Tin Học Tập", page_icon="🎓", layout="wide")

st.title("🎓 Chào mừng đến với Cổng Thông Tin")
st.write("Sử dụng Menu bên trái để vào Diễn đàn hoặc Đăng nhập.")
st.markdown("---")
st.subheader("🤖 Trợ Lý AI Học Tập")

# Đường link CDN chính hãng của Botpress (đã nhúng ID của fen)
# Đường link CDN chính hãng của Botpress (đã nhúng ID chuẩn)
import streamlit.components.v1 as components

# Đoạn mã JavaScript gốc của Botpress
botpress_code = """
<div style="height: 600px; width: 100%; position: relative;">
    <script src="https://cdn.botpress.cloud/webchat/v1/inject.js"></script>
    <script>
      window.botpressWebChat.init({
          "clientId": "32180f7e-9675-4570-91cb-fe856586b71f",
          "hostUrl": "https://cdn.botpress.cloud/webchat/v1",
          "messagingUrl": "https://messaging.botpress.cloud",
          "botName": "Trợ Lý AI",
          "hideWidget": false
      });
      
      /* Lệnh này ép khung chat tự động mở lên khi tải trang */
      window.botpressWebChat.onEvent(function (event) {
          if (event.type === 'LIFECYCLE.LOADED') {
              window.botpressWebChat.sendEvent({ type: 'show' });
          }
      }, ['LIFECYCLE.LOADED']);
    </script>
</div>
"""

# Nhúng thẳng mã HTML/JS vào Streamlit
components.html(botpress_code, height=650, scrolling=True)
