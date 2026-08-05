import streamlit as st

if not st.session_state.get("logged_in", False):
    st.error("⚠️ Bạn chưa đăng nhập! Vui lòng quay lại trang chính.")
    st.page_link("app.py", label="🔑 Quay lại Trang chủ", icon="👉")
    st.stop()

st.set_page_config(page_title="Trắc Nghiệm AI", page_icon="📝", layout="wide")

st.title("📝 Phòng Luyện Thi Trắc Nghiệm AI")
st.markdown("Hệ thống tự động tạo câu hỏi trắc nghiệm dựa trên kiến thức học tập của bạn.")
st.divider()

# Giao diện chọn môn luyện tập
col1, col2 = st.columns(2)
with col1:
    chon_mon = st.selectbox("📚 Chọn môn học:", ["Toán học", "Ngữ văn", "Tiếng Anh", "Khoa học Tự nhiên", "Lịch sử & Địa lý"])
with col2:
    muc_do = st.selectbox("⚡ Chọn mức độ:", ["Dễ (Cơ bản)", "Trung bình", "Khó (Nâng cao)"])

if st.button("🚀 Bắt đầu làm bài", type="primary", use_container_width=True):
    st.success(f"Đang tạo đề thi môn **{chon_mon}** với mức độ **{muc_do}** bằng AI...")
    
    # Giả lập câu hỏi trắc nghiệm
    st.markdown("---")
    st.markdown("### Câu 1: Đâu là thủ đô của Việt Nam?")
    ans = st.radio("Chọn đáp án đúng:", ["Hồ Chí Minh", "Hà Nội", "Đà Nẵng", "Cần Thơ"], key="q1")
    
    if st.button("Nộp bài câu này"):
        if ans == "Hà Nội":
            st.success("🎉 Chính xác! Bạn nhận được +10 điểm.")
        else:
            st.error("❌ Chưa chính xác. Đáp án đúng là Hà Nội.")

st.markdown("---")
st.page_link("app.py", label="🏠 Quay về Trang chủ", icon="⬅️")
