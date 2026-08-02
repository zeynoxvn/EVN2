import streamlit as st
import streamlit.components.v1 as components

# 1. Cấu hình trang
st.set_page_config(page_title="Hệ Thống Học Tập AI & Diễn Đàn", page_icon="🔒", layout="wide")

# 2. Khởi tạo trạng thái đăng nhập
if "da_dang_nhap" not in st.session_state:
    st.session_state.da_dang_nhap = False
if "ten_nguoi_dung" not in st.session_state:
    st.session_state.ten_nguoi_dung = ""

# ==========================================
# KHU VỰC 1: CHẶN CỬA (CHƯA ĐĂNG NHẬP)
# ==========================================
if not st.session_state.da_dang_nhap:
    st.title("🔒 Cổng Đăng Nhập Hệ Thống")
    st.markdown("Vui lòng đăng nhập hoặc tạo tài khoản mới để truy cập vào trợ lý AI và Diễn Đàn.")
    
    tab_dang_nhap, tab_dang_ky = st.tabs(["🔑 Đăng Nhập", "📝 Đăng Ký Tài Khoản"])
    
    with tab_dang_nhap:
        st.subheader("Đăng nhập vào tài khoản của bạn")
        email_dn = st.text_input("Email hoặc tên đăng nhập", key="input_email_dn")
        mat_khau_dn = st.text_input("Mật khẩu", type="password", key="input_mk_dn")
        
        if st.button("🚀 Đăng Nhập Ngay", type="primary", key="btn_dn"):
            if email_dn.strip() != "" and mat_khau_dn.strip() != "":
                st.session_state.da_dang_nhap = True
                st.session_state.ten_nguoi_dung = email_dn
                st.success("Đăng nhập thành công! Đang chuyển hướng...")
                st.rerun()
            else:
                st.error("Vui lòng nhập đầy đủ thông tin đăng nhập!")

    with tab_dang_ky:
        st.subheader("Đăng ký tài khoản học sinh mới")
        email_dk = st.text_input("Email của bạn", key="input_email_dk")
        mat_khau_dk = st.text_input("Mật khẩu mới", type="password", key="input_mk_dk")
        
        if st.button("✨ Đăng Ký Ngay", key="btn_dk"):
            if email_dk.strip() != "" and mat_khau_dk.strip() != "":
                st.success("Đăng ký thành công! Hãy sang tab Đăng Nhập để vào hệ thống.")
            else:
                st.warning("Vui lòng điền đầy đủ thông tin để đăng ký!")

# ==========================================
# KHU VỰC 2: BÊN TRONG (ĐÃ ĐĂNG NHẬP - CÓ BOTPRESS)
# ==========================================
else:
    # Thanh Sidebar
    with st.sidebar:
        st.write(f"👤 Xin chào, **{st.session_state.ten_nguoi_dung}**")
        if st.button("🚪 Đăng Xuất"):
            st.session_state.da_dang_nhap = False
            st.session_state.ten_nguoi_dung = ""
            st.rerun()
            
        st.markdown("---")
        st.markdown("### 🧭 Điều hướng")
        st.info("Bro có thể chọn các trang con (như Diễn Đàn) ở menu bên trái.")

    # Giao diện chính bên trong
    st.title("🤖 Trợ Giúp AI & Không Gian Học Tập")
    st.success("🎉 Chúc mừng bạn đã đăng nhập thành công vào hệ thống!")
    
    st.markdown("---")
    st.subheader("💬 Trò chuyện trực tiếp với Trợ lý AI (Botpress):")

    # --- NHÚNG CODE BOTPRESS CỦA BRO VÀO ĐÂY ---
    botpress_code = """
    <div style="height: 600px; width: 100%; position: relative;">
        <script src="https://cdn.botpress.cloud/webchat/v5.0/inject.js"></script>
        <script src="https://files.bpcontent.cloud/2026/08/01/04/20260801041109-K5GAT84Z.js" defer></script>
    </div>
    """
    
    # Hiển thị khung chat botpress lên web Streamlit
    components.html(botpress_code, height=650, scrolling=True)
