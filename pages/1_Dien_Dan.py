import streamlit as st
import requests
from src.moderation import cham_diem_vi_pham


# ==========================================
# 1. CẤU HÌNH TRANG & BIẾN TOÀN CỤC
# ==========================================
st.set_page_config(page_title="Diễn Đàn Học Sinh", page_icon="💬", layout="wide")

GSHEETS_URL = "https://script.google.com/macros/s/AKfycbzV0KqHng6Edeb8LupXLSY84M_v4VnenGHenVWj_d7pvzVlsq2KWwh7dN-xwOSP33oh/exec"
api_key = st.secrets.get("OPENAI_API_KEY", "") if "OPENAI_API_KEY" in st.secrets else ""

DANH_SACH_MON = ["Toán học", "Ngữ văn", "Tiếng Anh", "Khoa học Tự nhiên", "Lịch sử & Địa lý", "GDCD", "Khác"]

# ==========================================
# 2. HÀM XỬ LÝ DỮ LIỆU (API & GOOGLE SHEETS)
# ==========================================
@st.cache_data(ttl=5, show_spinner=False)
def fetch_posts(url):
    """Lấy danh sách bài viết từ Google Sheets."""
    if not url or "DÁN_LINK" in url:
        return []
    try:
        res = requests.get(url, timeout=5)
        return res.json() if res.status_code == 200 else []
    except Exception:
        return []

def send_to_sheets(payload):
    """Gửi dữ liệu lên Google Sheets với xử lý lỗi an toàn."""
    try:
        res = requests.post(GSHEETS_URL, json=payload, timeout=10)
        try:
            data = res.json()
            if isinstance(data, dict) and data.get("status") == "error":
                st.error(f"🚨 Báo lỗi từ máy chủ CSDL: {data.get('message')}")
                return False
            st.cache_data.clear()
            return True
        except Exception:
            st.error("🚨 Google không trả về dữ liệu hợp lệ! Vui lòng kiểm tra lại Web App URL.")
            return False
    except Exception as e:
        st.error(f"Lỗi mạng/kết nối: {e}")
        return False

# ==========================================
# 3. GIAO DIỆN CHUNG & SIDEBAR
# ==========================================
st.title("💬 Diễn Đàn Thảo Luận Học Sinh")
st.caption("Nơi trao đổi bài học an toàn - Tích hợp bộ lọc AI & Tiếng Việt đa lớp")

# Nút điều hướng
try:
    st.page_link("app.py", label="🏠 Quay về Trang Chủ", use_container_width=False)
except Exception:
    pass # Bỏ qua lỗi nếu không tìm thấy app.py khi test cục bộ

st.divider()

# Sidebar cài đặt
with st.sidebar:
    st.header("⚙️ Cài đặt")
    bypass_ai = st.checkbox("🛠️ Tạm tắt kiểm duyệt AI (Bypass)", value=False)
    if st.button("🔄 Tải lại dữ liệu mới"):
        st.cache_data.clear()
        st.rerun()

# ==========================================
# 4. KHU VỰC ĐĂNG BÀI MỚI
# ==========================================
st.subheader("✍️ Đăng bài thảo luận mới")

col1, col2 = st.columns(2)
with col1:
    mon_hoc = st.selectbox("📚 Chọn môn học:", ["Toán học", "Ngữ văn", "Tiếng Anh", "Lịch sử", "Địa lý"])
with col2:
    # Ô nhập nội dung
    noidung_thao_luan = st.text_area("📝 Nội dung thảo luận:", placeholder="Nhập câu hỏi hoặc ý kiến của bạn...")

# Xử lý khi bấm nút Đăng bài
if st.button("🚀 Đăng bài ngay", type="primary"):
    if noidung_thao_luan.strip() == "":
        st.warning("Vui lòng nhập nội dung bài viết trước khi đăng!")
    else:
        # Ném nội dung vào máy kiểm duyệt
        ket_qua = cham_diem_vi_pham(noidung_thao_luan)
        diem = ket_qua["diem_vi_pham"]
        
        # Xử lý dựa trên điểm số trả về
        if diem == 0:
            st.success(f"✅ Đăng bài thành công môn {mon_hoc}!")
            # Code lưu bài của bạn sẽ chạy ở đây
            
        elif diem <= 30:
            st.warning(f"⚠️ Bài viết đã đăng nhưng cần lưu ý: {ket_qua['hanh_dong_de_xuat']} (Điểm: {diem}/100)")
            # Code lưu bài của bạn sẽ chạy ở đây
            
        else:
            st.error(f"🚨 Bài viết bị chặn! {ket_qua['hanh_dong_de_xuat']} (Điểm vi phạm: {diem}/100)")
            st.write("**Hệ thống phát hiện các từ ngữ sau:**")
            st.json(ket_qua["chi_tiet"])
        # Gửi dữ liệu nếu qua vòng kiểm duyệt
        if should_post:
            with st.spinner("⚡ Đang tải bài viết lên diễn đàn..."):
                if send_to_sheets({"action": "add_post", "subject": subject, "content": user_input}):
                    st.success("✅ Đã đăng bài thành công!")
                    st.rerun()

st.divider()

# ==========================================
# 5. KHU VỰC HIỂN THỊ BÀI VIẾT (THEO TAB)
# ==========================================
st.subheader("📌 Bảng Tin Học Tập")
posts = fetch_posts(GSHEETS_URL)

danh_sach_tab = ["Tất cả"] + DANH_SACH_MON
tabs = st.tabs(danh_sach_tab)

for i, tab in enumerate(tabs):
    with tab:
        ten_tab = danh_sach_tab[i]
        
        # Phân loại bài viết
        if ten_tab == "Tất cả":
            bai_viet_hien_thi = posts
        else:
            bai_viet_hien_thi = [p for p in posts if p.get('subject', 'Khác') == ten_tab]
        
        # Hiển thị
        if not bai_viet_hien_thi:
            st.info(f"📭 Chưa có bài đăng nào trong chuyên mục {ten_tab}.")
        else:
            # SỬA LỖI Ở ĐÂY: Vòng lặp phải dùng `bai_viet_hien_thi` thay vì `posts`
            for idx, post in enumerate(bai_viet_hien_thi):
                with st.container():
                    # Hiển thị tiêu đề & nội dung
                    st.markdown(f"### 📘 {post.get('subject', 'Không có tiêu đề')}")
                    st.write(post.get('content', ''))
                    
                    # Hiển thị bình luận
                    comments = post.get('comments', [])
                    if comments:
                        st.caption("💬 Bình luận:")
                        for c in comments:
                            st.info(f"{c}")
                    
                    # Khung nhập bình luận
                    with st.expander("📝 Viết câu trả lời"):
                        # Tạo key duy nhất để tránh lỗi trùng lặp widget của Streamlit
                        safe_key = f"comment_{post.get('id', 'blank')}_{idx}_{i}"
                        
                        reply = st.text_input("Viết bình luận...", key=f"input_{safe_key}")
                        if st.button("Gửi bình luận", key=f"btn_{safe_key}"):
                            if reply.strip():
                                nguoi_dang = st.session_state.get('fullname', 'Ẩn danh')
                                binhluan_kem_ten = f"👤 **{nguoi_dang}**: {reply.strip()}"
                                
                                with st.spinner("Đang gửi..."):
                                    if send_to_sheets({
                                        "action": "add_comment", 
                                        "post_id": post.get("id"), 
                                        "comment": binhluan_kem_ten
                                    }):
                                        st.toast("✅ Đã gửi câu trả lời!")
                                        st.rerun()
                            else:
                                st.warning("Vui lòng nhập nội dung bình luận!")
                
                st.divider() # Ngăn cách giữa các bài viết
