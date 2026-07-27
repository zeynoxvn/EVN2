import streamlit as st
from google import genai

# Cấu hình trang Web
st.set_page_config(page_title="Diễn đàn Học tập AI", page_icon="🎓", layout="centered")

st.title("🎓 Diễn đàn Học sinh & Hỏi đáp AI")
st.caption("Nơi học sinh trao đổi bài học - Được kiểm duyệt an toàn bởi Gemini AI")

# Thanh nhập API Key ở menu bên trái
st.sidebar.header("🔑 Cấu hình")
api_key = st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password")

# Khởi tạo lưu trữ bài đăng tạm thời trong bộ nhớ
if "posts" not in st.session_state:
    st.session_state.posts = []

st.subheader("✍️ Đăng câu hỏi / Bình luận mới")
subject = st.selectbox("Chọn môn học:", ["Toán học", "Ngữ văn", "Tiếng Anh", "Vật lý", "Hóa học", "Lịch sử & Địa lý", "Khác"])
user_input = st.text_area("Nội dung thảo luận của bạn:", placeholder="Nhập câu hỏi hoặc ý kiến bài học ở đây...")

if st.button("🚀 Đăng bài", type="primary"):
    if not api_key:
        st.error("⚠️ Bro cần nhập Gemini API Key ở góc bên trái (Sidebar) trước nhé!")
    elif not user_input.strip():
        st.warning("⚠️ Vui lòng nhập nội dung trước khi đăng!")
    else:
        with st.spinner("🤖 Gemini AI đang kiểm duyệt nội dung..."):
            try:
                # Kết nối API Gemini
                client = genai.Client(api_key=api_key)
                prompt = f"""
                Bạn là hệ thống kiểm duyệt nội dung cho diễn đàn học sinh phổ thông.
                Hãy phân tích đoạn văn bản sau: "{user_input}".
                - Nếu an toàn, lịch sự và phù hợp với học sinh, chỉ trả về đúng 1 từ: APPROVED
                - Nếu chứa ngôn từ xúc phạm, chửi thề, toxic hoặc không phù hợp, trả về: REJECTED | [Lý do ngắn gọn]
                """
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=prompt
                )
                res_text = response.text.strip()

                if "APPROVED" in res_text:
                    st.success("✅ Bài viết hợp lệ và đã đăng lên diễn đàn!")
                    # Lưu bài đăng
                    st.session_state.posts.insert(0, {"subject": subject, "content": user_input})
                else:
                    st.error("❌ Bài viết bị từ chối do vi phạm quy chuẩn cộng đồng!")
                    st.info(f"Phản hồi từ AI: {res_text}")
            except Exception as e:
                st.error(f"Lỗi kết nối Gemini API: {e}")

st.divider()
st.subheader("📌 Danh sách bài đăng trên diễn đàn")

if not st.session_state.posts:
    st.info("Chưa có bài đăng nào. Hãy là người đầu tiên đặt câu hỏi!")
else:
    for post in st.session_state.posts:
        with st.container(border=True):
            st.markdown(f"**[{post['subject']}]**")
            st.write(post['content'])
