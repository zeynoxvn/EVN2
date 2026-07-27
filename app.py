import streamlit as st
from google import genai

# Cấu hình trang Web
st.set_page_config(page_title="Dien dan Hoc tap AI", page_icon="🎓", layout="centered")

st.title("🎓 Diễn đàn Học sinh & Hỏi đáp AI")
st.caption("Nơi học sinh trao đổi bài học - Được kiểm duyệt an toàn bởi Gemini AI")

# Thanh nhập API Key
st.sidebar.header("Cấu hình")
api_key = st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password").strip()

if "posts" not in st.session_state:
    st.session_state.posts = []

st.subheader("Đăng câu hỏi / Bình luận mới")
subject = st.selectbox("Chọn môn học:", ["Toán học", "Ngữ văn", "Tiếng Anh", "Vật lý", "Hóa học", "Lịch sử & Địa lý", "Khác"])
user_input = st.text_area("Nội dung thảo luận của bạn:", placeholder="Nhập câu hỏi hoặc ý kiến bài học ở đây...")

if st.button("Đăng bài", type="primary"):
    if not api_key:
        st.error("Bro cần nhập Gemini API Key ở góc bên trái trước nhé!")
    elif not user_input.strip():
        st.warning("Vui lòng nhập nội dung trước khi đăng!")
    else:
        with st.spinner("Gemini AI đang kiểm duyệt nội dung..."):
            try:
                client = genai.Client(api_key=api_key)
                prompt = f"""
                Ban la he thong kiem duyet noi dung cho dien dan hoc sinh.
                Phan tich doan van ban sau: "{user_input}".
                - Neu an toan, lich su va phu hop: chi tra ve dung 1 tu: APPROVED
                - Neu chua ngon tu xuc pham, toxic, vi pham: tra ve: REJECTED
                """
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=prompt
                )
                res_text = response.text.strip()

                if "APPROVED" in res_text:
                    st.success("Bài viết hợp lệ và đã đăng lên diễn đàn!")
                    st.session_state.posts.insert(0, {"subject": subject, "content": user_input})
                else:
                    st.error("Bài viết bị từ chối do vi phạm quy chuẩn cộng đồng!")
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    st.error("Hệ thống tạm thời hết lượt API hoặc quá tải. Bro vui lòng thử lại sau 1 phút hoặc tạo API Key ở Project mới!")
                else:
                    st.error(f"Lỗi kết nối Gemini API: {err_str}")

st.divider()
st.subheader("Danh sách bài đăng trên diễn đàn")

if not st.session_state.posts:
    st.info("Chưa có bài đăng nào. Hãy là người đầu tiên đặt câu hỏi!")
else:
    for post in st.session_state.posts:
        with st.container(border=True):
            st.markdown(f"**[{post['subject']}]**")
            st.write(post['content'])
