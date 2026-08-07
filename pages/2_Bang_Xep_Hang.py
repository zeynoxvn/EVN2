import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Bảng Xếp Hạng", page_icon="🏆")

# ==========================================
# KHÓA CỬA BẢNG XẾP HẠNG
# ==========================================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Khu vực hạn chế: Bạn chưa báo danh!")
    st.info("Vui lòng quay lại trang Đăng Nhập để xem Bảng Vàng nhé.")
    st.stop()

# --- ĐIỀN LINK API CỦA BRO VÀO ĐÂY ---
API_URL = "https://script.google.com/macros/s/AKfycbzV0KqHng6Edeb8LupXLSY84M_v4VnenGHenVWj_d7pvzVlsq2KWwh7dN-xwOSP33oh/exec" 

st.title("🏆 BẢNG VÀNG VINH DANH")
st.markdown("Nơi tụ hội của những cao thủ Toán học đỉnh nhất trường!")
st.markdown("---")

# Hàm xét hạng Rank 
def get_rank_info(score):
    if score <= 100:
        return "Tân binh", "🥉"
    elif score <= 300:
        return "Học giả", "🥈"
    elif score <= 600:
        return "Tinh anh", "🥇"
    else:
        return "Thách đấu", "💎"

# Lấy dữ liệu từ server
with st.spinner("Đang tải dữ liệu Bảng xếp hạng..."):
    try:
        response = requests.post(API_URL, json={"action": "get_leaderboard"}).json()
        
        if response.get("status") == "success":
            leaderboard_data = response["data"]
            
            if len(leaderboard_data) > 0:
                # --- HIỂN THỊ TOP 3 CAO THỦ ---
                st.subheader("🌟 TOP 3 CAO THỦ XUẤT SẮC NHẤT 🌟")
                top3_cols = st.columns(3)
                
                for i in range(min(3, len(leaderboard_data))):
                    player = leaderboard_data[i]
                    rank_name, rank_icon = get_rank_info(player['score'])
                    medal = ["🥇 TOP 1", "🥈 TOP 2", "🥉 TOP 3"][i]
                    
                    with top3_cols[i]:
                        st.markdown(f"""
                        <div style='text-align: center; padding: 15px; border-radius: 10px; background-color: #262730; border: 1px solid #4CAF50;'>
                            <h3 style='color: #FFD700;'>{medal}</h3>
                            <h4>{player['fullname']}</h4>
                            <h2 style='color: #4CAF50;'>{player['score']} đ</h2>
                            <p style='font-size: 18px;'>{rank_icon} {rank_name}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.write("")
                st.write("")
                
                # --- HIỂN THỊ DANH SÁCH CÒN LẠI ---
                st.subheader("📜 Danh sách anh tài")
                
                # Chuẩn bị dữ liệu cho bảng
                table_data = []
                for idx, p in enumerate(leaderboard_data):
                    rank_name, rank_icon = get_rank_info(p['score'])
                    table_data.append({
                        "Hạng": f"#{idx + 1}",
                        "Họ và Tên": p['fullname'],
                        "Điểm số": p['score'],
                        "Danh hiệu": f"{rank_icon} {rank_name}"
                    })
                
                # Hiển thị bảng bằng Pandas DataFrame cho đẹp
                df = pd.DataFrame(table_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
            else:
                st.info("Chưa có cao thủ nào ghi danh trên bảng xếp hạng!")
        else:
            st.error(f"Lỗi hệ thống: {response.get('message')}")
            
    except Exception as e:
        st.error("Không thể kết nối đến máy chủ. Vui lòng thử lại sau!")
