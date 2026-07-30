import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang
st.set_page_config(page_title="Cổng Thông Tin THCS Sông Ray", page_icon="🎓", layout="wide")

# Menu bên trái
st.sidebar.title("📌 MENU CHÍNH")
page = st.sidebar.radio("Vui lòng chọn tính năng:", [
    "🏠 Trang Chủ", 
    "🔑 Đăng Nhập / Đăng Ký", 
    "💬 Diễn Đàn Thảo Luận", 
    "⚙️ Quản Trị Hệ Thống (Admin)",
    "🤖 Trợ Lý AI (Sông Ray)"
])

# Trang AI riêng biệt
if page == "🤖 Trợ Lý AI (Sông Ray)":
    st.title("🤖 Trợ Lý AI Học Tập - THCS Sông Ray")
    st.caption("Trợ lý AI sẵn sàng giải đáp mọi thắc mắc học tập của bạn 24/7.")
    st.markdown("---")
    
    # Code chatbot chuẩn
    coze_code = """
    <script src="https://sf-cdn.coze.com/obj/unpkg-va/flow-platform/chat-app-sdk/1.2.0-beta.6/libs/oversea/index.js"></script>
    <script>
      new CozeWebSDK.WebChatClient({
        config: { bot_id: '7668150083120185349' },
        componentProps: { title: 'Trợ lý Sông Ray' },
        auth: {
          type: 'token',
          token: 'DÁN_MÃ_PAT_CỦA_FEN_VÀO_ĐÂY',
          onRefreshToken: function () {
            return 'DÁN_MÃ_PAT_CỦA_FEN_VÀO_ĐÂY'
          }
        }
      });
    </script>
    """
    components.html(coze_code, height=650)

# Các trang khác
elif page == "🏠 Trang Chủ":
    st.title("🎓 Cổng Thông Tin & Diễn Đàn Học Tập THCS")
    st.write("Chào mừng bạn đến với hệ thống hỗ trợ học tập trực tuyến tích hợp AI!")
else:
    st.title(f"Trang {page}")
    st.write("Tính năng đang được phát triển...")
