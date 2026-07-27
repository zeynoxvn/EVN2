import streamlit as st
import requests
from google import genai

# 1. Cấu hình trang & Giao diện nâng cao
st.set_page_config(
    page_title="Diễn đàn Học tập THCS", 
    page_icon="🎓", 
    layout="wide"
)

# Custom CSS làm đẹp giao diện
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stCard {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border: 1px solid #e9ecef;
    }
    .badge-subject {
        background-color: #e3f2fd;
        color: #0d47a1;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .comment-box {
        background-color: #f1f3f5;
        border-left: 3px solid #228be6;
        padding: 8px 12px;
        border-radius: 4px;
        margin-top: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# 🔴 DÁN LINK GOOGLE APPS SCRIPT CỦA BRO VÀO ĐÂY:
GSHEETS_URL = "https://script.google.com/macros/s/AKfycbwGBEYfr81KO32Zip_tD07tF5daLkyWTwYZy6px8YurboD0bhbiG0NzlVQ59qW-JN-h/exec"
# Header Diễn đàn
st.title("🎓 Diễn đàn Học sinh & Hỏi đáp AI")
st.caption("Nơi học sinh trao đổi bài học - Kiểm duyệt an toàn bởi Gemini AI")

# Sidebar Cấu hình
with st.sidebar:
    st.header("⚙️ Cấu hình Hệ thống")
    api_key = st.text_input("🔑 Nhập Gemini API Key:", type="password").strip()
    selected_model = st.selectbox("🤖 Mô hình AI:", ["gemini-2.0-flash", "gemini-2.0-flash-lite"])
    bypass_ai = st.checkbox("🛠️ Bật chế độ Test (Tắt lọc AI)")
    st.divider()
    st.info("💡 **Mẹo:** Học sinh có thể chọn chủ đề theo từng thẻ môn học ở giao diện chính để dễ tìm bài viết!")

# Hàm tải dữ liệu
def load_posts():
    try:
        res = requests.get(GSHEETS_URL, timeout=10)
        return res.json()
    except Exception:
        return []

# Khu vực Đăng bài
st.subheader("✍️ Đăng bài thảo luận mới")
col1, col2 = st.columns([1, 2])

with col1:
    subject = st.selectbox(
        "📚 Chọn môn học:", 
        ["Toán học", "Ngữ văn", "Tiếng Anh", "Vật lý", "Hóa học", "Lịch sử & Địa lý", "Khác"]
    )

with col2:
    user_input = st.text_area("📝 Nội dung thảo luận:", placeholder="Nhập thắc mắc hoặc nội dung bài học ở đây...", height=100)

if st.button("🚀 Đăng lên diễn đàn", type="primary", use_container_width=True):
    if not user_input.strip():
        st.warning("Vui lòng nhập nội dung trước khi đăng!")
    elif bypass_ai:
        requests.post(GSHEETS_URL, json={"action": "add_post", "subject": subject, "content": user_input})
        st.success("✅ [Chế độ Test] Bài viết đã đăng thành công!")
        st.rerun()
    else:
        if not api_key:
            st.error("Bro cần nhập Gemini API Key ở thanh bên trái trước nhé!")
        else:
            with st.spinner("🤖 AI đang kiểm duyệt nội dung..."):
                try:
                    client = genai.Client(api_key=api_key)
                    prompt = f"""
                    Ban la he thong kiem duyet noi dung cho dien dan hoc sinh THCS.
                    Phan tich van ban: "{user_input}".
                    - Neu an toan, phu hop hoc duong: tra ve dung 1 tu: APPROVED
                    - Neu xuc pham, toxic, vi pham: tra ve: REJECTED
                    """
                    response = client.models.generate_content(model=selected_model, contents=prompt)
                    if "APPROVED" in response.text.strip():
                        requests.post(GSHEETS_URL, json={"action": "add_post", "subject": subject, "content": user_input})
                        st.success("✅ Bài viết hợp lệ và đã đăng thành công!")
                        st.rerun()
                    else:
                        st.error("❌ Bài viết bị từ chối do vi phạm quy chuẩn cộng đồng học đường!")
                except Exception as e:
                    st.error(f"Lỗi kết nối API: {e}")

st.divider()

# Bảng dữ liệu bài đăng & Thẻ Tabs phân loại
posts = load_posts()

# Thanh thống kê nhỏ
col_stat1, col_stat2 = st.columns(2)
col_stat1.metric("📊 Tổng số bài thảo luận", len(posts))
col_stat2.metric("🟢 Trạng thái CSDL", "Google Sheets Online")

st.subheader("📌 Dòng thời gian thảo luận")

# Tạo các Tabs môn học
tab_all, tab_toan, tab_van, tab_geog, tab_other = st.tabs(
    ["🌐 Tất cả", "📐 Toán học", "📖 Ngữ văn", "🌍 Lịch sử & Địa lý", "📌 Môn khác"]
)

def render_post_list(post_list):
    if not post_list:
        st.info("Chưa có bài đăng nào trong mục này.")
        return
        
    for post in post_list:
        with st.container():
            st.markdown(f"""
            <div class="stCard">
                <span class="badge-subject">📚 {post['subject']}</span>
                <p style="font-size: 1.1rem; margin-top: 10px; color: #212529;">{post['content']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Hiển thị bình luận
            if "comments" in post and post["comments"]:
                st.caption("💬 Phản hồi từ học sinh / giáo viên:")
                for comment in post["comments"]:
                    st.markdown(f'<div class="comment-box">👉 {comment}</div>', unsafe_allow_html=True)
            
            # Trả lời
            with st.expander("💬 Viết phản hồi cho bài này"):
                reply = st.text_input("Nội dung câu trả lời:", key=f"in_{post['id']}")
                if st.button("Gửi bình luận", key=f"btn_{post['id']}"):
                    if reply.strip():
                        requests.post(GSHEETS_URL, json={
                            "action": "add_comment", 
                            "post_id": post["id"], 
                            "comment": reply.strip()
                        })
                        st.success("Đã gửi phản hồi!")
                        st.rerun()
            st.write("")

# Lọc bài đăng theo Tabs
with tab_all:
    render_post_list(posts)

with tab_toan:
    render_post_list([p for p in posts if p.get('subject') == 'Toán học'])

with tab_van:
    render_post_list([p for p in posts if p.get('subject') == 'Ngữ văn'])

with tab_geog:
    render_post_list([p for p in posts if p.get('subject') == 'Lịch sử & Địa lý'])

with tab_other:
    render_post_list([p for p in posts if p.get('subject') not in ['Toán học', 'Ngữ văn', 'Lịch sử & Địa lý']])
