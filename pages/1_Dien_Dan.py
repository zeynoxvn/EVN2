import streamlit as st
import requests
from src.moderation import moderate_content

# 1. Cấu hình trang
st.set_page_config(page_title="Diễn Đàn Học Sinh", page_icon="💬", layout="wide")

# 🔴 DÁN LINK APPS SCRIPT CỦA BRO VÀO ĐÂY:
GSHEETS_URL = "https://script.google.com/macros/s/AKfycbzV0KqHng6Edeb8LupXLSY84M_v4VnenGHenVWj_d7pvzVlsq2KWwh7dN-xwOSP33oh/exec"

# Tự động lấy API Key của OpenAI từ két sắt Streamlit Secrets
api_key = st.secrets.get("OPENAI_API_KEY", "") if "OPENAI_API_KEY" in st.secrets else ""

# Danh sách các môn học chuẩn theo chương trình
DANH_SACH_MON = ["Toán học", "Ngữ văn", "Tiếng Anh", "Khoa học Tự nhiên", "Lịch sử & Địa lý", "GDCD", "Khác"]

st.title("💬 Diễn Đàn Thảo Luận Học Sinh")
st.caption("Nơi trao đổi bài học an toàn - Tích hợp bộ lọc AI & Tiếng Việt đa lớp")

# Nút quay về Trang chủ
st.page_link("app.py", label="🏠 Quay về Trang Chủ", use_container_width=False)
st.divider()

# Cấu hình bypass AI (chỉ dùng khi lỗi)
bypass_ai = st.sidebar.checkbox("🛠️ Tạm tắt kiểm duyệt (Bypass)", value=False)
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
# Hàm gửi dữ liệu (Đã gắn thêm siêu bắt lỗi)
def send_to_sheets(payload):
    try:
        res = requests.post(GSHEETS_URL, json=payload, timeout=10)
        try:
            data = res.json()
            # Nếu Google báo lỗi, in thẳng ra web
            if isinstance(data, dict) and data.get("status") == "error":
                st.error(f"🚨 Báo lỗi từ máy chủ CSDL: {data.get('message')}")
                return False
            st.cache_data.clear()
            return True
        except Exception:
            st.error("🚨 Google không trả về dữ liệu! Có thể fen quên Deploy New Version rồi!")
            return False
    except Exception as e:
        st.error(f"Lỗi mạng/kết nối: {e}")
        return False

# ==========================================
# KHU VỰC ĐĂNG BÀI MỚI
# ==========================================
st.subheader("✍️ Đăng bài thảo luận mới")
col1, col2 = st.columns([1, 2])

with col1:
    subject = st.selectbox("📚 Chọn môn học:", DANH_SACH_MON)

with col2:
    user_input = st.text_area("📝 Nội dung thảo luận:", placeholder="Nhập câu hỏi hoặc ý kiến của bạn...", height=120)

if st.button("🚀 Đăng bài ngay", type="primary", use_container_width=True):
    if not user_input.strip():
        st.warning("Vui lòng nhập nội dung bài viết!")
    else:
        should_post = False
        
        if bypass_ai:
            should_post = True
        else:
            with st.spinner("🛡️ Hệ thống đang kiểm duyệt nội dung..."):
                mod_result = moderate_content(text=user_input, api_key=api_key, strikes=0, force_ai=False)
                
                if mod_result.action == "allow":
                    should_post = True
                else:
                    st.error(f"❌ Bài viết không được duyệt! (Hành động: {mod_result.action.upper()})")
                    st.warning(f"**Lý do:** {mod_result.reason}")
                    if mod_result.excerpt:
                        st.info(f"**Từ ngữ nghi vấn:** `{mod_result.excerpt}`")

        if should_post:
            with st.spinner("⚡ Đang tải bài viết lên diễn đàn..."):
                if send_to_sheets({"action": "add_post", "subject": subject, "content": user_input}):
                    st.success("✅ Bài viết an toàn! Đã đăng thành công.")
                    st.rerun()

st.divider()

# ==========================================
# KHU VỰC HIỂN THỊ BÀI VIẾT THEO TAB MÔN HỌC
# ==========================================
posts = fetch_posts(GSHEETS_URL)
st.subheader(f"📌 Bảng Tin Học Tập")

# Tạo danh sách Tab (Thêm mục "Tất cả" lên đầu tiên)
danh_sach_tab = ["Tất cả"] + DANH_SACH_MON
tabs = st.tabs(danh_sach_tab)

# Lặp qua từng tab để hiển thị dữ liệu
for i, tab in enumerate(tabs):
    with tab:
        ten_tab = danh_sach_tab[i]
        
        # Lọc bài viết theo môn học của Tab hiện tại
        if ten_tab == "Tất cả":
            bai_viet_hien_thi = posts
        else:
            bai_viet_hien_thi = [p for p in posts if p.get('subject', 'Khác') == ten_tab]
        
        # Hiển thị giao diện bài viết
        if not bai_viet_hien_thi:
            st.info(f"Chưa có bài đăng nào trong chuyên mục {ten_tab}.")
        else:
            for idx, post in enumerate(bai_viet_hien_thi):
                with st.container(border=True):
                    # Hiển thị môn học màu xanh cho nổi bật
                    st.markdown(f"**Khoa Khoa / Chủ đề:** :blue[{post.get('subject', 'Khác')}]")
                    st.write(post.get('content', ''))
                    
                    # Hiển thị bình luận
                    comments = post.get('comments', [])
                    if comments:
                        st.caption("💬 Bình luận:")
                        for c_idx, c in enumerate(comments):
                            # Chia 2 cột: 1 bên hiện bình luận, 1 bên hiện nút chấm điểm (nếu là thầy giáo)
                            col_c1, col_c2 = st.columns([5, 1])
                            
                            with col_c1:
                                st.info(f"{c}")
                                
                            with col_c2:
                                # BẢO MẬT: Chỉ hiện nút chấm điểm nếu tên đăng nhập là phanle
                                if st.session_state.get("username") == "phanle":
                                    # Trích xuất tên học sinh từ chuỗi bình luận
                                    if c.startswith("👤 **"):
                                        try:
                                            student_name = c.split("**")[1]
                                            # Nút bấm cộng điểm
                                            if st.button("✅ +5đ", key=f"score_{post.get('id', idx)}_{c_idx}", help=f"Thưởng 5 điểm cho {student_name}"):
                                                with st.spinner("⏳..."):
                                                    # Gửi lệnh cộng điểm lên Google Sheets
                                                    if send_to_sheets({"action": "add_score", "fullname": student_name, "points": 5}):
                                                        st.toast(f"🎉 Đã cộng 5 điểm cho {student_name}!")
                                        except Exception:
                                            pass
                    
                    # Khung trả lời (thêm ten_tab vào key để không bị lỗi trùng lặp mã khi chuyển tab)
                    with st.expander("📝 Viết câu trả lời"):
                            reply = st.text_input("Viết bình luận...", key=f"cmt_{post.get('id', idx)}")
                            if st.button("Gửi bình luận", key=f"btn_cmt_{post.get('id', idx)}"):
                                if reply:
                                    # Lấy tên người đang đăng nhập dán vào bình luận
                                    nguoi_dang = st.session_state.get('fullname', 'Ẩn danh')
                                    binhluan_kem_ten = f"👤 **{nguoi_dang}**: {reply.strip()}"
                                    
                                    with st.spinner("Đang gửi..."):
                                        # Gửi cái bình luận đã có gắn tên lên Google Sheets
                                        if send_to_sheets({"action": "add_comment", "post_id": post.get("id"), "comment": binhluan_kem_ten}):
                                            st.toast("✅ Đã gửi câu trả lời!")
                                            st.rerun()
