import streamlit as st
# Đặt đoạn này ở đầu các file trang con trong thư mục pages/
if not st.session_state.get("logged_in", False):
    st.error("⚠️ Bạn chưa đăng nhập! Vui lòng quay lại trang chính để đăng nhập trước khi sử dụng tính năng này.")
    st.page_link("app.py", label="🔑 Quay lại Trang chủ để Đăng nhập", icon="👉")
    st.stop() # Dừng không cho chạy tiếp nội dung bên dưới
import json
from src.moderation import moderate_content

# Cấu hình giao diện
st.set_page_config(page_title="Admin Kiểm Duyệt", page_icon="🛡️", layout="wide")

st.title("🛡️ Bảng Điều Khiển Kiểm Duyệt (Admin)")

# 🏠 THÊM NÚT QUAY VỀ TRANG CHỦ Ở ĐÂY CHO TIỆN
st.page_link("app.py", label="🏠 Quay về Trang Chủ", icon="⬅️")
st.divider()

# ==========================================
# 🛑 Ổ KHÓA BẢO MẬT (CHỈ ADMIN MỚI ĐƯỢC VÀO)
# ==========================================
password_guess = st.text_input("🔑 Nhập mật khẩu Admin để truy cập:", type="password")

# ĐỔI MẬT KHẨU CỦA FEN Ở ĐÂY NHÉ
if password_guess != "andung123":
    st.error("⛔ Bạn không có quyền truy cập trang này. Vui lòng nhập đúng mật khẩu!")
    st.stop()

st.success("✅ Đăng nhập thành công! Chào mừng Admin.")
st.divider()

# --- NẾU NHẬP ĐÚNG MẬT KHẨU ---
st.caption("Giao diện UI tách biệt hoàn toàn - Code xử lý đã nằm gọn trong thư mục src/")

with st.sidebar:
    st.header("⚙️ Cấu hình hệ thống")
    st.subheader("👤 Giả lập Người dùng")
    user_strikes = st.number_input("Số lần vi phạm trước đó:", min_value=0, max_value=10, value=0)
    force_ai = st.checkbox("🤖 Ép dùng AI (Bỏ qua bộ lọc tĩnh)", value=False)
    st.markdown("---")
    # Thêm nút về trang chủ ở sidebar luôn cho mượt
    st.page_link("app.py", label="🏠 Về Trang Chủ", icon="⚡")

st.subheader("📝 Nhập bài đăng cần test")
user_input = st.text_area("Nội dung:", height=150, placeholder="Ví dụ: Đăng ký ngay để nhận thưởng, click link...")

admin_api_key = st.secrets.get("OPENAI_API_KEY", "") if "OPENAI_API_KEY" in st.secrets else ""

if st.button("🚀 Chạy Test Hệ Thống", type="primary", use_container_width=True):
    if not user_input.strip():
        st.warning("Vui lòng nhập văn bản!")
    else:
        with st.spinner("Hệ thống đang quét đa lớp..."):
            result = moderate_content(
                text=user_input, 
                api_key=admin_api_key, 
                strikes=user_strikes,
                force_ai=force_ai
            )
            
            st.divider()
            color = "green" if result.label == "SAFE" else "orange" if result.label == "SUSPICIOUS" else "red"
            st.markdown(f"### 🎯 Kết quả: <span style='color:{color}'>{result.label}</span>", unsafe_allow_html=True)
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Hành động xử lý", result.action.upper())
            c2.metric("Điểm vi phạm", f"{result.severity}/100")
            c3.metric("Phân loại", result.category)
            c4.metric("Engine đã dùng", "AI" if result.used_ai else "Bộ lọc tĩnh")
            
            with st.container(border=True):
                st.write(f"**Lý do:** {result.reason}")
                if result.excerpt:
                    st.write(f"**Đoạn vi phạm:** `{result.excerpt}`")
            
            st.subheader("📦 Payload JSON (Dữ liệu ngầm):")
            st.json(result.model_dump())
