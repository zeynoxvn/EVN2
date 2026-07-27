import streamlit as st
import json
from src.moderation import moderate_content

# Cấu hình giao diện
st.set_page_config(page_title="Admin Kiểm Duyệt", page_icon="🛡️", layout="wide")

st.title("🛡️ Bảng Điều Khiển Kiểm Duyệt (Admin)")
st.caption("Giao diện UI tách biệt hoàn toàn - Code xử lý đã nằm gọn trong thư mục src/")

# Menu cài đặt bên trái
with st.sidebar:
    st.header("⚙️ Cấu hình hệ thống")
    # Ô nhập API Key để test (nhập API key của bro vào đây khi dùng)
    ui_api_key = st.text_input("🔑 Nhập Gemini API Key:", type="password")
    ui_api_key = st.text_input("🔑 Nhập OpenAI API Key:", type="password")
    
    st.divider()
    st.subheader("👤 Giả lập Người dùng")
    user_strikes = st.number_input("Số lần vi phạm trước đó:", min_value=0, max_value=10, value=0)
    force_ai = st.checkbox("🤖 Ép dùng AI (Bỏ qua bộ lọc tĩnh)", value=False)
    
    st.info("💡 Nếu không có API Key, web vẫn chạy bằng Bộ Lọc Tĩnh (Rule-based) quét từ bậy.")

# Khu vực nhập văn bản
st.subheader("📝 Nhập bài đăng cần test")
user_input = st.text_area("Nội dung:", height=150, placeholder="Ví dụ: Đăng ký ngay để nhận thưởng, click link...")

# Nút bấm - Giao diện chỉ gọi 1 dòng lệnh duy nhất tới "nhà bếp"
if st.button("🚀 Chạy Test Hệ Thống", type="primary", use_container_width=True):
    if not user_input.strip():
        st.warning("Vui lòng nhập văn bản!")
    else:
        with st.spinner("Hệ thống đang quét đa lớp..."):
            
            # --- ĐÂY LÀ DÒNG GỌI LOGIC TỪ THƯ MỤC SRC/ ---
            result = moderate_content(
                text=user_input, 
                api_key=ui_api_key, 
                strikes=user_strikes,
                force_ai=force_ai
            )
            
            # --- PHẦN DƯỚI NÀY CHỈ LÀ VẼ GIAO DIỆN HIỂN THỊ TRỰC QUAN ---
            st.divider()
            
            color = "green" if result.label == "SAFE" else "orange" if result.label == "SUSPICIOUS" else "red"
            st.markdown(f"### 🎯 Kết quả: <span style='color:{color}'>{result.label}</span>", unsafe_allow_html=True)
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Hành động xử lý", result.action.upper())
            c2.metric("Điểm vi phạm", f"{result.severity}/100")
            c3.metric("Phân loại", result.category)
            c4.metric("Engine đã dùng", "AI (Gemini)" if result.used_ai else "Bộ lọc tĩnh")
            
            with st.container(border=True):
                st.write(f"**Lý do:** {result.reason}")
                if result.excerpt:
                    st.write(f"**Đoạn vi phạm:** `{result.excerpt}`")
            
            st.subheader("📦 Payload JSON (Dữ liệu ngầm):")
            st.json(result.model_dump())
