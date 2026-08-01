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
bot_url = 'https://cdn.botpress.cloud/webchat/v1/index.html?options=%7B%22clientId%22%3A%2232180f7e-9675-4570-91cb-fe856586b71f%22%7D'

# Nhúng thẳng khung chat nguyên bản vào web
components.iframe(bot_url, height=650, scrolling=True)
