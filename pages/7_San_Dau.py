import streamlit as st
import requests
import time

st.set_page_config(page_title="Sàn Đấu Toán Học", page_icon="⚔️")
st.page_link("app.py", label="🏠 Quay lại Trang chủ", icon="⬅️")
st.markdown("---")

# --- ĐIỀN LINK API CỦA BRO VÀO ĐÂY ---
API_URL = "https://script.google.com/macros/s/AKfycbzV0KqHng6Edeb8LupXLSY84M_v4VnenGHenVWj_d7pvzVlsq2KWwh7dN-xwOSP33oh/exec" 
THOI_GIAN_THI = 60 

# KHÓA CỬA SÀN ĐẤU
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Khu vực hạn chế: Bạn chưa báo danh!")
    st.stop() 

# Lấy tên người chơi (nếu có lưu lúc đăng nhập)
player_name = st.session_state.get("username", "Cao thủ ẩn danh")

st.title("⚔️ Sàn Đấu Toán Học")
st.markdown(f"Chào mừng **{player_name}** đến với đấu trường trí tuệ!")

# KHỞI TẠO BỘ NHỚ
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "is_playing" not in st.session_state:
    st.session_state.is_playing = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "match_ended" not in st.session_state:
    st.session_state.match_ended = False
if "total_score" not in st.session_state:
    st.session_state.total_score = 0

# HÀM XÉT HẠNG RANK
def get_rank_name(score):
    if score <= 100:
        return "🥉 Tân binh (Rank Đồng)"
    elif score <= 300:
        return "🥈 Học giả (Rank Bạc)"
    elif score <= 600:
        return "🥇 Tinh anh (Rank Vàng)"
    else:
        return "💎 Thách đấu (Rank Kim Cương)"

# HÀM LẤY ĐỀ THI
def fetch_questions():
    with st.spinner("Đang xáo trộn đề..."):
        try:
            payload = {"action": "get_match_questions", "limit": 5}
            response = requests.post(API_URL, json=payload).json()
            
            if response.get("status") == "success":
                st.session_state.questions = response["data"]
                st.session_state.current_q = 0
                st.session_state.score = 0
                st.session_state.start_time = time.time()
                st.session_state.is_playing = True
                st.session_state.match_ended = False
                st.rerun() 
            else:
                st.error(f"Lỗi từ máy chủ: {response.get('message')}")
        except Exception as e:
            st.error(f"Lỗi kết nối API: {e}")

# HÀM GỬI ĐIỂM LÊN SERVER KHI KẾT THÚC
def update_score_to_server():
    with st.spinner("Đang đồng bộ điểm số lên hệ thống..."):
        try:
            payload = {
                "action": "update_score",
                "username": player_name, 
                "points": st.session_state.score
            }
            response = requests.post(API_URL, json=payload).json()
            if response.get("status") == "success":
                # Lấy tổng điểm mới từ Google Sheets trả về
                st.session_state.total_score = response.get("new_total", st.session_state.score)
                st.toast("Đã lưu điểm thành công! ☁️", icon="✅")
            else:
                st.error(f"Lỗi lưu điểm: {response.get('message')}")
        except Exception as e:
            st.error("Không thể lưu điểm lúc này, vui lòng kiểm tra kết nối mạng.")

# HÀM CHẤM ĐIỂM
def check_answer(selected_option, correct_answer):
    time_elapsed = time.time() - st.session_state.start_time
    if time_elapsed > THOI_GIAN_THI:
        st.warning("⏰ Ối! Bạn đã trả lời sau khi hết thời gian!")
    else:
        if selected_option == correct_answer:
            st.session_state.score += 10
            st.toast("Chính xác! +10 điểm 🎉", icon="✅")
        else:
            st.toast(f"Sai rồi! Đáp án đúng là {correct_answer} ❌", icon="🚨")
    st.session_state.current_q += 1

# === GIAO DIỆN THI ĐẤU ===
if not st.session_state.is_playing and not st.session_state.match_ended:
    st.info(f"Bạn có {THOI_GIAN_THI} giây để hoàn thành 5 câu hỏi.")
    if st.button("🚀 BẮT ĐẦU CÀY RANK", use_container_width=True, type="primary"):
        fetch_questions()

# MÀN HÌNH TỔNG KẾT & VINH DANH RANK
elif st.session_state.match_ended:
    st.success("🏁 Trận đấu kết thúc!")
    st.balloons()
    
    # Lấy tên Rank dựa trên tổng điểm
    rank_name = get_rank_name(st.session_state.total_score)
    
    st.markdown(f"""
    <div style='text-align: center; padding: 20px; background-color: #1E1E1E; border-radius: 10px; margin-bottom: 20px;'>
        <h3>Điểm trận này</h3>
        <h1 style='color: #FFD700; font-size: 40px;'>+{st.session_state.score} 🏆</h1>
        <hr>
        <h4>Tổng điểm tích lũy của bạn</h4>
        <h2 style='color: #4CAF50;'>{st.session_state.total_score}</h2>
        <h3 style='color: #00BCD4;'>Danh hiệu: {rank_name}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Tiếp tục cày Rank", use_container_width=True):
        fetch_questions()

# TRONG LÚC ĐANG THI ĐẤU
else:
    time_elapsed = time.time() - st.session_state.start_time
    time_left = max(0, THOI_GIAN_THI - int(time_elapsed))
    
    # Kiểm tra điều kiện nộp bài (hết giờ hoặc hết câu)
    if time_left == 0 or st.session_state.current_q >= len(st.session_state.questions):
        st.session_state.is_playing = False
        st.session_state.match_ended = True
        update_score_to_server() # Bắn điểm lên Sheets
        st.rerun() # Tải lại trang để nhảy sang Màn hình tổng kết
    else:
        q = st.session_state.questions[st.session_state.current_q]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Tiến độ", f"Câu {st.session_state.current_q + 1} / {len(st.session_state.questions)}")
        col2.metric("Điểm hiện tại", f"{st.session_state.score} 🏆")
        col3.metric("⏳ Thời gian còn", f"{time_left} s")
        
        st.progress(time_left / THOI_GIAN_THI)
        
        st.subheader(f"❓ {q['question']}")
        st.caption(f"Độ khó: {q['level']}")
        st.write("") 
        
        opt_col1, opt_col2 = st.columns(2)
        with opt_col1:
            if st.button(f"A. {q['opt_a']}", use_container_width=True):
                check_answer("A", q['answer'])
                st.rerun()
            if st.button(f"C. {q['opt_c']}", use_container_width=True):
                check_answer("C", q['answer'])
                st.rerun()
        with opt_col2:
            if st.button(f"B. {q['opt_b']}", use_container_width=True):
                check_answer("B", q['answer'])
                st.rerun()
            if st.button(f"D. {q['opt_d']}", use_container_width=True):
                check_answer("D", q['answer'])
                st.rerun()
