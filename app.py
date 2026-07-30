import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Cổng Thông Tin THCS Sông Ray",
    page_icon="🎓",
    layout="wide"
)

st.sidebar.title("📌 MENU CHÍNH")
page = st.sidebar.radio(
    "Vui lòng chọn tính năng:",
    [
        "🏠 Trang Chủ", 
        "🔑 Đăng Nhập / Đăng Ký", 
        "💬 Diễn Đàn Thảo Luận", 
        "⚙️ Quản Trị Hệ Thống (Admin)",
        "🤖 Trợ Lý AI (Sông Ray)"
    ]
)

if page == "🏠 Trang Chủ":
    st.title("🎓 Cổng Thông Tin & Diễn Đàn Học Tập THCS")
    st.write("Chào mừng bạn đến với hệ thống hỗ trợ học tập trực tuyến tích hợp AI!")
    st.info("Nơi trao đổi kiến thức và giải đáp thắc mắc về môn Địa lý và các môn học khác.")
    
    # Bọc lệnh tải ảnh trong khối try-except để web không bị sập nếu ảnh bị lỗi định dạng
    try:
        st.image("banner_thcs_song_ray.png", use_container_width=True)
    except Exception:
        st.warning("⚠️ Không thể tải ảnh Banner (Định dạng ảnh chưa chuẩn).")

elif page == "🔑 Đăng Nhập / Đăng Ký":
    st.title("🔑 Đăng Nhập / Đăng Ký Tài Khoản")
    st.write("Tính năng đăng nhập dành cho học sinh và giáo viên (Đang phát triển).")

elif page == "💬 Diễn Đàn Thảo Luận":
    st.title("💬 Diễn Đàn Thảo Luận Học Tập")
    st.write("Nơi học sinh đặt câu hỏi và thảo luận bài học (Đang phát triển).")

elif page == "⚙️ Quản Trị Hệ Thống (Admin)":
    st.title("⚙️ Quản Trị Hệ Thống")
    st.write("Khu vực dành riêng cho Quản trị viên.")

elif page == "🤖 Trợ Lý AI (Sông Ray)":
    st.title("🤖 Trợ Lý AI Học Tập - THCS Sông Ray")
    st.caption("Trợ lý AI sẵn sàng giải đáp mọi thắc mắc học tập của bạn 24/7.")
    st.markdown("---")

    # Mã nhúng Coze Chatbot tối giản (Tự động nhận diện khách vãng lai)
 coze_code = """
    <script src="https://sf-cdn.coze.com/obj/unpkg-va/flow-platform/chat-app-sdk/1.2.0-beta.6/libs/oversea/index.js"></script>
    <script>
      new CozeWebSDK.WebChatClient({
        config: { bot_id: '7668150083120185349' },
        componentProps: { title: 'Trợ lý Sông Ray' },
        auth: {
          type: 'token',
          token: 'pat_ZH2rOPbcUTQPiiKjlh7WvyjqzqUGhPddJrFgJw24ZrT5M5P61nQjzhxrj9ukYaXf',
          onRefreshToken: function () {
            return 'DÁN_MÃ_PAT_CỦA_FEN_VÀO_ĐÂY'
          }
        }
      });
    </script>
    """
    
