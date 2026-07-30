import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang
st.set_page_config(page_title="Cổng Thông Tin & Trợ Lý AI", page_icon="🎓", layout="wide")

# Giao diện Trang chủ
st.title("🎓 Chào mừng đến với Cổng Thông Tin")
st.write("Sử dụng Menu bên trái để vào Diễn đàn hoặc Đăng nhập.")
st.markdown("---")
st.subheader("👇 KHU VỰC CỦA TRỢ LÝ AI (Nhìn xuống góc dưới bên phải)")

# Code nhúng Coze chatbot bản quốc tế (bắt buộc dùng Token)
coze_code = """
<script src="https://sf-cdn.coze.com/obj/unpkg-va/flow-platform/chat-app-sdk/1.2.0-beta.6/libs/oversea/index.js"></script>
<script>
  new CozeWebSDK.WebChatClient({
    config: { bot_id: '7668150083120185349' },
    componentProps: { title: 'Trợ lý Sông Ray' },
    auth: {
      type: 'token',
      token: 'DÁN_MÃ_PAT_CỦA_FEN_VÀO_ĐÂY',
      onRefreshToken: function () {
        return 'DÁN_MÃ_PAT_CỦA_FEN_VÀO_ĐÂY'
      }
    }
  });
</script>
"""

# Gọi khung HTML ẩn để kích hoạt Bot
components.html(coze_code, height=600)
