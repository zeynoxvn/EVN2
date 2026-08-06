import streamlit as st
import requests

# Kiểm tra đăng nhập
if not st.session_state.get("logged_in", False):
    st.error("⚠️ Bạn chưa đăng nhập! Vui lòng quay lại trang chính.")
    st.page_link("app.py", label="🔑 Quay lại Trang chủ để Đăng nhập", icon="👉")
    st.stop()

st.set_page_config(page_title="Quản Lý Kết Bạn", page_icon="👥", layout="wide")

# Link Google Apps Script của bro
GSHEETS_URL = "https://script.google.com/macros/s/AKfycbzV0KqHng6Edeb8LupXLSY84M_v4VnenGHenVWj_d7pvzVlsq2KWwh7dN-xwOSP33oh/exec"
current_user = st.session_state.get("username", "")

st.title("👥 Kết Nối & Quản Lý Bạn Bè")
st.markdown("Tìm kiếm bạn học, gửi lời mời kết bạn và mở rộng vòng kết nối học tập của bạn.")
st.divider()

# Hàm gọi API lấy dữ liệu bạn bè & lời mời chờ
def get_friend_data():
    try:
        res = requests.post(GSHEETS_URL, json={
            "action": "get_friends",
            "username": current_user
        }, timeout=10)
        return res.json()
    except Exception:
        return {"status": "error", "pending": [], "friends": []}

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🔍 Tìm kiếm bạn bè")
    search_user = st.text_input("Nhập tên đăng nhập (Username) của bạn bè:")
    
    if st.button("Gửi lời mời kết bạn", type="primary", use_container_width=True):
        if not search_user.strip():
            st.warning("Vui lòng nhập tên tài khoản cần tìm!")
        elif search_user.strip() == current_user:
            st.error("Bạn không thể tự kết bạn với chính mình!")
        else:
            with st.spinner("Đang gửi lời mời..."):
                try:
                    res = requests.post(GSHEETS_URL, json={
                        "action": "send_friend_request",
                        "sender": current_user,
                        "receiver": search_user.strip()
                    }, timeout=10)
                    data = res.json()
                    if data.get("status") == "success":
                        st.success("✅ Đã gửi lời mời kết bạn thành công!")
                        st.rerun()
                    else:
                        st.error(data.get("message", "Không thể gửi lời mời."))
                except Exception as e:
                    st.error(f"Lỗi kết nối: {e}")

    st.markdown("---")
    st.subheader("📥 Lời mời kết bạn đang chờ")
    
    friend_data = get_friend_data()
    pending_list = friend_data.get("pending", [])
    
    if not pending_list:
        st.info("Chưa có lời mời kết bạn nào mới.")
    else:
        for p in pending_list:
            req_id = p.get("id")
            sender_name = p.get("sender")
            
            with st.container(border=True):
                # Đã sửa lỗi: Xóa dấu trừ thừa ở đây
                st.write(f"👤 **{sender_name}** muốn kết bạn với bạn.")
                if st.button("✅ Chấp nhận", key=f"accept_{req_id}"):
                    with st.spinner("Đang xử lý..."):
                        try:
                            res = requests.post(GSHEETS_URL, json={
                                "action": "accept_friend",
                                "request_id": req_id
                            }, timeout=10)
                            data = res.json()
                            if data.get("status") == "success":
                                st.success("Đã đồng ý kết bạn!")
                                st.rerun()
                            else:
                                st.error(data.get("message"))
                        except Exception as e:
                            st.error(f"Lỗi: {e}")

with col2:
    st.subheader("🤝 Danh sách bạn bè của bạn")
    
    friends_list = friend_data.get("friends", [])
    if not friends_list:
        st.info("Bạn chưa có người bạn nào trong danh sách.")
    else:
        for f in friends_list:
            f_name = f.get("friend")
            with st.container(border=True):
                col_name, col_btn = st.columns([3, 1])
                
                with col_name:
                    st.write(f"👤 **{f_name}** (Bạn bè)")
                
                with col_btn:
                    if st.button("💬 Nhắn", key=f"chat_{f_name}"):
                        st.session_state.chat_with = f_name
                        st.switch_page("pages/6_Nhan_Tin.py")

st.markdown("---")
st.page_link("app.py", label="🏠 Quay về Trang chủ", icon="⬅️")
