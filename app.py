import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang
st.set_page_config(page_title="THCS Sông Ray", page_icon="🎓", layout="wide")

st.title("🎓 Chào mừng đến với Cổng Thông Tin THCS Sông Ray")
st.write("Sử dụng Menu bên trái để truy cập các tính năng như Diễn đàn, Đăng nhập và Trợ lý AI.")

# Nếu fen muốn giữ con AI ở trang chủ luôn thì để đây
st.markdown("---")
st.subheader("🤖 Trợ Lý AI Học Tập")

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
components.html(coze_code, height=650)
