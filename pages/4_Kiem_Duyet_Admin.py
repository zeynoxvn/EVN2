import streamlit as st
import json
from src.moderation import moderate_content

# Cấu hình giao diện
st.set_page_config(page_title="Admin Kiểm Duyệt", page_icon="🛡️", layout="wide")

st.title("🛡️ Bảng Điều Khiển Kiểm Duyệt (Admin)")

# ==========================================
# 🛑 Ổ KHÓA BẢO MẬT (CHỈ ADMIN MỚI ĐƯỢC VÀO)
# ==========================================
password_guess = st.text_input("🔑 Nhập mật khẩu Admin để truy cập:", type="password")

# ĐỔI MẬT KHẨU CỦA FEN Ở ĐÂY NHÉ (thay chữ admin123 thành pass fen muốn)
if password_guess != "andung123":
    st.error("⛔ Bạn không có quyền truy cập trang này. Vui lòng nhập đúng mật khẩu!")
    st.stop() # Lệnh này sẽ chặn đứng không cho chạy bất kỳ code nào bên dưới

st.success("✅ Đăng nhập thành công! Chào mừng Admin.")
st.divider()
# ==========================================


# --- NẾU NHẬP ĐÚNG MẬT KHẨU, GIAO DIỆN DƯỚI NÀY MỚI HIỆN RA ---
st.caption("Giao diện UI tách biệt hoàn toàn - Code xử lý đã nằm gọn trong thư mục src/")

# Menu cài đặt bên trái
with st.sidebar:
    st.header("⚙️ Cấu hình hệ thống")
    st.subheader("👤 Giả lập Người dùng")
    user_strikes = st.number_input("Số lần vi phạm trước đó:", min_value=0, max_value=10, value=0)
    force_ai = st.checkbox("🤖 Ép dùng AI (Bỏ qua bộ lọc tĩnh)", value=False)
    
    st.info("💡 Hệ thống đang sử dụng OpenAI Moderation (Miễn phí 100%) kết hợp Bộ lọc Tiếng Việt tĩnh.")

# Khu vực nhập văn bản
st.subheader("📝 Nhập bài đăng cần test")
user_input = st.text_area("Nội dung:", height=150, placeholder="Ví dụ: Đăng ký ngay để nhận thưởng, click link...")

# Tự động lấy API Key của OpenAI từ két sắt Streamlit Secrets
admin_api_key = st.secrets.get("OPENAI_API_KEY", "") if "OPENAI_API_KEY" in st.secrets else ""

# Nút bấm - Giao diện chỉ gọi 1 dòng lệnh duy nhất tới "nhà bếp"
if st.button("🚀 Chạy Test Hệ Thống", type="primary", use_container_width=True):
    if not user_input.strip():
        st.warning("Vui lòng nhập văn bản!")
    else:
        with st.spinner("Hệ thống đang quét đa lớp..."):
            
            # GỌI LOGIC TỪ THƯ MỤC SRC/
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
