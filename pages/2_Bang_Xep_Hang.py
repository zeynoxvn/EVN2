import streamlit as st
import pandas as pd

if not st.session_state.get("logged_in", False):
    st.error("⚠️ Bạn chưa đăng nhập! Vui lòng quay lại trang chính.")
    st.page_link("app.py", label="🔑 Quay lại Trang chủ", icon="👉")
    st.stop()

st.set_page_config(page_title="Bảng Xếp Hạng", page_icon="🏆", layout="wide")

st.title("🏆 Bảng Xếp Hạng Học Tập & Tương Tác")
st.markdown("Vinh danh những thành viên tích cực nhất hệ thống EVN by AN,DŨNG.")
st.divider()

# Tạo bảng dữ liệu mẫu phong cách chuyên nghiệp
df_ranking = pd.DataFrame({
    "Hạng": ["🥇 1", "🥈 2", "🥉 3", "4", "5"],
    "Thành viên": ["Nguyễn Văn An", "Lê Thị Hiền Lương", "Trần Minh Dũng", "Phạm Hoàng Long", "Vũ Thu Trang"],
    "Điểm Hoạt Động": [1250, 1120, 980, 850, 790],
    "Bài viết đóng góp": [24, 19, 15, 12, 10],
    "Danh hiệu": ["Cao Thủ AI", "Chuyên Gia", "Tích Cực", "Thành Viên", "Thành Viên"]
})

st.dataframe(df_ranking, use_container_width=True, hide_index=True)

st.markdown("---")
st.page_link("app.py", label="🏠 Quay về Trang chủ", icon="⬅️")
