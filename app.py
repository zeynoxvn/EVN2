from streamlit_autorefresh import st_autorefresh

# Tự động làm mới dữ liệu sau mỗi 10.000 ms (10 giây)
st_autorefresh(interval=10000, limit=None, key="auto_refresh_posts")
import streamlit as st
import requests
from google import genai

# Cấu hình trang Web
st.set_page_config(page_title="Diễn đàn Học tập", page_icon="🎓", layout="wide")

# 🔴 DÁN LINK WEBSCRIPT CỦA BRO VÀO ĐÂY:
GSHEETS_URL = "https://script.google.com/macros/s/AKfycbxZ-TDInG9E45qk2p6rjuJz19_RipcRBlGvmFEWk6YhCWQgFhg9GGKi-hlBpHApjsZL/exec"

st.title("🎓 Diễn đàn Học sinh & Hỏi đáp AI")
st.caption("Nơi học sinh trao đổi bài học - Kết nối Google Sheets & Gemini AI")

# Sidebar
st.sidebar.header("⚙️ Cấu hình")
api_key = st.sidebar.text_input("🔑 Nhập Gemini API Key:", type="password").strip()
selected_model = st.sidebar.selectbox("🤖 Mô hình AI:", ["gemini-2.0-flash", "gemini-2.0-flash-lite"])
bypass_ai = st.sidebar.checkbox("🛠️ Bật chế độ Test (Tắt lọc AI)", value=True)

# Hàm lấy bài viết từ Google Sheets
def load_posts():
    if not GSHEETS_URL or "DÁN_LINK" in GSHEETS_URL:
        st.warning("⚠️ Bro chưa dán link GSHEETS_URL vào dòng 9 trong code app.py!")
        return []
    try:
        res = requests.get(GSHEETS_URL, timeout=10)
        if res.status_code == 200:
            try:
                return res.json()
            except Exception:
                st.error("⚠️ Google Sheets trả về dữ liệu không đúng định dạng. Bro kiểm tra lại Bước 1 tạo bản Triển khai MỚI nhé!")
                return []
        else:
            st.error(f"⚠️ Không thể kết nối Google Sheets. Mã lỗi: {res.status_code}")
            return []
    except Exception as e:
        st.error(f"⚠️ Lỗi kết nối Google Sheets: {e}")
        return []

# Hàm gửi bài đăng lên Google Sheets
def send_post_to_sheets(subject, content):
    try:
        res = requests.post(GSHEETS_URL, json={"action": "add_post", "subject": subject, "content": content}, timeout=15)
        if res.status_code in [200, 302]:
            st.success("✅ Đã ghi nhận bài viết thành công!")
            return True
        else:
            st.error(f"❌ Gửi bài thất bại! Mã phản hồi từ Google: {res.status_code}")
            return False
    except Exception as e:
        st.error(f"❌ Lỗi khi gửi dữ liệu lên Google Sheets: {e}")
        return False

# Giao diện Đăng bài
st.subheader("✍️ Đăng bài thảo luận mới")
col1, col2 = st.columns([1, 2])

with col1:
    subject = st.selectbox("📚 Chọn môn học:", ["Toán học", "Ngữ văn", "Tiếng Anh", "Vật lý", "Hóa học", "Lịch sử & Địa lý", "Khác"])

with col2:
    user_input = st.text_area("📝 Nội dung thảo luận:", placeholder="Nhập thắc mắc hoặc bài học...", height=100)

if st.button("🚀 Đăng lên diễn đàn", type="primary", use_container_width=True):
    if not user_input.strip():
        st.warning("Vui lòng nhập nội dung trước khi đăng!")
    elif bypass_ai:
        if send_post_to_sheets(subject, user_input):
            st.rerun()
    else:
        if not api_key:
            st.error("Bro cần nhập Gemini API Key hoặc tích chọn 'Bật chế độ Test' ở thanh bên trái!")
        else:
            with st.spinner("🤖 Gemini AI đang kiểm duyệt nội dung..."):
                try:
                    client = genai.Client(api_key=api_key)
                    prompt = f'Ban la he thong kiem duyet noi dung hoc sinh. Phan tich: "{user_input}". Neu an toan tra ve APPROVED, neu vi pham tra ve REJECTED.'
                    response = client.models.generate_content(model=selected_model, contents=prompt)
                    
                    if "APPROVED" in response.text.strip():
                        if send_post_to_sheets(subject, user_input):
                            st.rerun()
                    else:
                        st.error("❌ Bài viết bị từ chối do vi phạm quy chuẩn cộng đồng!")
                except Exception as e:
                    st.error(f"Lỗi AI: {e}")

st.divider()

# Hiển thị bài viết
posts = load_posts()
st.subheader(f"📌 Danh sách bài đăng ({len(posts)})")

if not posts:
    st.info("Chưa có bài đăng nào trên diễn đàn.")
else:
    for idx, post in enumerate(posts):
        with st.container(border=True):
            st.markdown(f"**[{post.get('subject', 'Khác')}]**")
            st.write(post.get('content', ''))
            
            # Hiển thị bình luận
            if post.get('comments'):
                st.caption("💬 Các bình luận:")
                for c in post['comments']:
                    st.info(f"👉 {c}")
            
            # Trả lời
            with st.expander("💬 Trả lời bài này"):
                reply = st.text_input("Nhập câu trả lời:", key=f"rep_{post.get('id', idx)}")
                if st.button("Gửi bình luận", key=f"btn_{post.get('id', idx)}"):
                    if reply.strip():
                        requests.post(GSHEETS_URL, json={"action": "add_comment", "post_id": post.get('id'), "comment": reply.strip()})
                        st.success("Đã gửi phản hồi!")
                        st.rerun()
