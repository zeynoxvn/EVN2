import streamlit as st
import requests
from google import genai

# Cấu hình trang Web
st.set_page_config(page_title="Diễn đàn Học tập Siêu Tốc", page_icon="⚡", layout="wide")

# 🔴 DÁN LINK APPS SCRIPT CỦA BRO VÀO ĐÂY:
GSHEETS_URL = "DÁN_LINK_APPS_SCRIPT_CỦA_BRO_VÀO_ĐÂY"

st.title("⚡ Diễn đàn Học sinh & Hỏi đáp AI (Tốc độ cao)")

# Sidebar Cấu hình
st.sidebar.header("⚙️ Cấu hình")
api_key = st.sidebar.text_input("🔑 Nhập Gemini API Key:", type="password").strip()
selected_model = st.sidebar.selectbox("🤖 Mô hình AI:", ["gemini-2.0-flash-lite", "gemini-2.0-flash"])
bypass_ai = st.sidebar.checkbox("🛠️ Bật chế độ Test (Tắt lọc AI)", value=True)

if st.sidebar.button("🔄 Tải lại dữ liệu mới"):
    st.cache_data.clear()
    st.rerun()

# 🚀 TỐI ƯU 1: Caching dữ liệu trong 5 giây (Tải web cực nhanh)
@st.cache_data(ttl=5, show_spinner=False)
def fetch_posts_from_sheets(url):
    if not url or "DÁN_LINK" in url:
        return []
    try:
        res = requests.get(url, timeout=5)
        return res.json() if res.status_code == 200 else []
    except Exception:
        return []

# Hàm gửi dữ liệu lên Google Sheets
def send_to_sheets(payload):
    try:
        requests.post(GSHEETS_URL, json=payload, timeout=5)
        # Xóa bộ nhớ đệm để lần sau lấy dữ liệu mới nhất
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Lỗi lưu CSDL: {e}")
        return False

# Khu vực Đăng bài
st.subheader("✍️ Đăng bài thảo luận mới")
col1, col2 = st.columns([1, 2])

with col1:
    subject = st.selectbox("📚 Chọn môn học:", ["Toán học", "Ngữ văn", "Tiếng Anh", "Vật lý", "Hóa học", "Lịch sử & Địa lý", "Khác"])

with col2:
    user_input = st.text_area("📝 Nội dung thảo luận:", placeholder="Nhập thắc mắc...", height=100)

if st.button("🚀 Đăng bài ngay", type="primary", use_container_width=True):
    if not user_input.strip():
        st.warning("Vui lòng nhập nội dung!")
    else:
        should_post = False
        
        if bypass_ai:
            should_post = True
        else:
            if not api_key:
                st.error("Chưa nhập API Key!")
            else:
                with st.spinner("⚡ AI đang duyệt siêu tốc..."):
                    try:
                        client = genai.Client(api_key=api_key)
                        # Prompt cực ngắn để AI trả lời nhanh nhất
                        res = client.models.generate_content(
                            model=selected_model, 
                            contents=f"Text: '{user_input}'. Is safe for school? Reply ONLY 'YES' or 'NO'."
                        )
                        if "YES" in res.text.upper():
                            should_post = True
                        else:
                            st.error("❌ Bài viết bị từ chối do nội dung không phù hợp!")
                    except Exception as e:
                        st.error(f"Lỗi AI: {e}")

        if should_post:
            with st.spinner("⚡ Đang lưu bài đăng..."):
                if send_to_sheets({"action": "add_post", "subject": subject, "content": user_input}):
                    st.success("✅ Đã đăng thành công!")
                    st.rerun()

st.divider()

# Hiển thị bài viết
posts = fetch_posts_from_sheets(GSHEETS_URL)
st.subheader(f"📌 Các bài thảo luận ({len(posts)})")

if not posts:
    st.info("Chưa có bài đăng nào.")
else:
    for idx, post in enumerate(posts):
        with st.container(border=True):
            st.markdown(f"**[{post.get('subject', 'Môn khác')}]**")
            st.write(post.get('content', ''))
            
            # Hiển thị bình luận
            comments = post.get('comments', [])
            if comments:
                st.caption("💬 Các bình luận:")
                for c in comments:
                    st.info(f"👉 {c}")
            
            # Trả lời nhanh
            with st.expander("💬 Viết câu trả lời"):
                reply = st.text_input("Nội dung:", key=f"rep_{post.get('id', idx)}")
                if st.button("Gửi bình luận", key=f"btn_{post.get('id', idx)}"):
                    if reply.strip():
                        with st.spinner("⚡ Đang gửi..."):
                            send_to_sheets({
                                "action": "add_comment", 
                                "post_id": post.get('id'), 
                                "comment": reply.strip()
                            })
                            st.success("Đã trả lời!")
                            st.rerun()
