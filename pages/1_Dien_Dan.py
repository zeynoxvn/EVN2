import streamlit as st
import requests
from src.moderation import moderate_content

# 1. Cấu hình trang
st.set_page_config(page_title="Diễn Đàn Học Sinh", page_icon="💬", layout="wide")

# 🔴 DÁN LINK APPS SCRIPT CỦA BRO VÀO ĐÂY:
GSHEETS_URL = "https://script.google.com/macros/s/AKfycbzaHudThpp-NN1_0EyAZqASl_uN9pcjBmW_BVMSddGI8KI0cRNYRdq6tpgrtJsyPzr_/exec"

st.title("💬 Diễn Đàn Thảo Luận Học Sinh")
st.caption("Nơi trao đổi bài học an toàn - Tích hợp bộ lọc AI & Tiếng Việt đa lớp")

# Nút quay về Trang chủ
st.page_link("app.py", label="🏠 Quay về Trang Chủ", use_container_width=False)
st.divider()

# Sidebar Cấu hình
st.sidebar.header("⚙️ Cấu hình Kiểm Duyệt")
api_key = st.sidebar.text_input("🔑 Nhập OpenAI API Key (Tùy chọn):", type="password").strip()
bypass_ai = st.sidebar.checkbox("🛠️ Bật chế độ Test (Tắt kiểm duyệt)", value=False)

if st.sidebar.button("🔄 Tải lại dữ liệu mới"):
    st.cache_data.clear()
    st.rerun()

# Hàm lấy bài viết từ Google Sheets
@st.cache_data(ttl=5, show_spinner=False)
def fetch_posts(url):
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
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Lỗi lưu CSDL: {e}")
        return False

# Khung Đăng bài
st.subheader("✍️ Đăng bài thảo luận mới")
col1, col2 = st.columns([1, 2])

with col1:
    subject = st.selectbox("📚 Chọn môn học:", ["Toán học", "Ngữ văn", "Tiếng Anh", "Vật lý", "Hóa học", "Lịch sử & Địa lý", "Khác"])

with col2:
    user_input = st.text_area("📝 Nội dung thảo luận:", placeholder="Nhập câu hỏi hoặc ý kiến của bạn...", height=120)

if st.button("🚀 Đăng bài ngay", type="primary", use_container_width=True):
    if not user_input.strip():
        st.warning("Vui lòng nhập nội dung bài viết!")
    else:
        should_post = False
        
        # Nếu bật chế độ bypass -> Cho đăng luôn
        if bypass_ai:
            should_post = True
        else:
            with st.spinner("🛡️ Hệ thống đang kiểm duyệt nội dung..."):
                # GỌI BỘ LỌC TỪ THƯ MỤC SRC/ (Ưu tiên bộ lọc Tiếng Việt trước)
                mod_result = moderate_content(
                    text=user_input,
                    api_key=api_key,
                    strikes=0,
                    force_ai=False
                )
                
                # Kiểm tra kết quả
                if mod_result.action == "allow":
                    should_post = True
                else:
                    st.error(f"❌ Bài viết không được duyệt! (Hành động: {mod_result.action.upper()})")
                    st.warning(f"**Lý do:** {mod_result.reason}")
                    if mod_result.excerpt:
                        st.info(f"**Từ ngữ nghi vấn:** `{mod_result.excerpt}`")

        # Thực hiện lưu nếu bài viết sạch
        if should_post:
            with st.spinner("⚡ Đang tải bài viết lên diễn đàn..."):
                if send_to_sheets({"action": "add_post", "subject": subject, "content": user_input}):
                    st.success("✅ Bài viết an toàn! Đã đăng thành công.")
                    st.rerun()

st.divider()

# Danh sách bài viết trên diễn đàn
posts = fetch_posts(GSHEETS_URL)
st.subheader(f"📌 Bài thảo luận mới nhất ({len(posts)})")

if not posts:
    st.info("Chưa có bài đăng nào trên diễn đàn.")
else:
    for idx, post in enumerate(posts):
        with st.container(border=True):
            st.markdown(f"**[{post.get('subject', 'Môn khác')}]**")
            st.write(post.get('content', ''))
            
            comments = post.get('comments', [])
            if comments:
                st.caption("💬 Bình luận:")
                for c in comments:
                    st.info(f"👉 {c}")
            
            with st.expander("💬 Viết câu trả lời"):
                reply = st.text_input("Nội dung bình luận:", key=f"rep_{post.get('id', idx)}")
                if st.button("Gửi bình luận", key=f"btn_{post.get('id', idx)}"):
                    if reply.strip():
                        # Kiểm duyệt cả bình luận trước khi cho gửi
                        reply_check = moderate_content(text=reply, api_key=api_key)
                        if reply_check.action == "allow":
                            with st.spinner("⚡ Đang gửi..."):
                                send_to_sheets({"action": "add_comment", "post_id": post.get('id'), "comment": reply.strip()})
                                st.success("Đã trả lời!")
                                st.rerun()
                        else:
                            st.error("Bình luận chứa từ ngữ không phù hợp!")
