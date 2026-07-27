import streamlit as st

st.set_page_config(page_title="Cổng Học Tập THCS", page_icon="🎓", layout="wide")

st.title("🎓 Cổng Thông Tin & Học Tập AI")
st.caption("Chào mừng bạn đến với hệ thống hỗ trợ học tập trực tuyến!")

st.divider()
st.subheader("🚀 Chọn tính năng bạn muốn sử dụng:")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("### 💬 Diễn Đàn Thảo Luận")
        st.write("Nơi đặt câu hỏi, trao đổi bài học cùng bạn bè và giáo viên. Tích hợp AI kiểm duyệt an toàn.")
        # 🟢 Dùng tên file không chứa emoji:
        st.page_link("pages/1_Dien_Dan.py", label="Truy cập Diễn đàn", icon="💬", use_container_width=True)

with col2:
    with st.container(border=True):
        st.markdown("### 🏆 Bảng Xếp Hạng")
        st.write("Xem bảng tổng kết điểm thi đua, phong trào học tập tích cực của các thành viên.")
        st.page_link("pages/2_Bang_Xep_Hang.py", label="Xem Bảng xếp hạng", icon="🏆", use_container_width=True)

with col3:
    with st.container(border=True):
        st.markdown("### 📝 Ôn Tập Trắc Nghiệm")
        st.write("Tự luyện tập câu hỏi trắc nghiệm các môn học do Gemini AI tạo đề tự động.")
        st.page_link("pages/3_Trac_Nghiem_AI.py", label="Thử sức ngay", icon="📝", use_container_width=True)
