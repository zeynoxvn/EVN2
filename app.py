import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang
st.set_page_config(page_title="Cổng Thông Tin Học Tập", page_icon="🎓", layout="wide")

st.title("🎓 Chào mừng đến với Cổng Thông Tin")
st.write("Sử dụng Menu bên trái để vào Diễn đàn hoặc Đăng nhập.")
st.markdown("---")
st.subheader("🤖 Trợ Lý AI Học Tập")

# Đường link trực tiếp đến thẳng con Bot của fen
bot_url = "https://mediafiles.botpress.cloud/32180f7e-9675-4570-91cb-fe856586b71f/webchat/bot.html"

# Khoét lỗ nhúng trực tiếp link vào web, dẹp bỏ mọi lỗi HTML
components.iframe(bot_url, height=650, scrolling=True)
