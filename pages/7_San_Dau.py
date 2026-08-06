import streamlit as st
import requests
import time

st.set_page_config(page_title="Sàn Đấu Toán Học", page_icon="⚔️")
st.page_link("app.py", label="🏠 Quay lại Trang chủ", icon="⬅️")
st.markdown("---")

# --- ĐIỀN LINK API CỦA FEN VÀO ĐÂY ---
API_URL = "https://script.google.com/macros/s/AKfycbzV0KqHng6Edeb8LupXLSY84M_v4VnenGHenVWj_d7pvzVlsq2KWwh7dN-xwOSP33oh/exec" 
THOI_GIAN_THI = 60 # Ví dụ: 60 giây cho 5 câu

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Khu vực hạn chế: Bạn chưa báo danh!")
    st.stop() 

st.title("⚔️ Sàn Đấu Toán Học")
st.markdown("Chào mừng các cao thủ đến với đấu trường trí tuệ!")

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

def fetch_questions():
    with st.spinner("Đang xáo trộn đề..."):
        try:
            payload = {"action": "get_match_questions", "limit": 5}
            response = requests.post(API_URL, json=payload).json()
            
            if response.get("status") == "success":
                st.session_state.questions = response["data"]
                st.session_state.current_q = 0
                st.session_state.score = 0
                st.session_state.is_playing = True
                st.session_state.start_time = time.time() # Bắt đầu tính giờ
                st.rerun() 
            else:
                st.error(f"Lỗi từ máy chủ: {response.get('message')}")
        except Exception as e:
            st.error(f"Lỗi kết nối API: {e}")

def check_answer(selected_option, correct_answer):
    if selected_option == correct_answer:
        st.session_state.score += 10
        st.toast("Chính xác! +10 điểm 🎉", icon="✅")
    else:
        st.toast(f"Sai rồi! Đáp án đúng là {correct_answer} ❌", icon="🚨")
    st.session_state.current_q += 1

# === GIAO DIỆN THI ĐẤU ===
if not st.session_state.is_playing:
    st.info(f"Bạn có {THOI_GIAN_THI} giây để hoàn thành 5 câu hỏi.")
    if st.button("🚀 BẮT ĐẦU THI ĐẤU", use_container_width=True, type="primary"):
        fetch_questions()
else:
    # TÍNH TOÁN THỜI GIAN
    time_elapsed = time.time() - st.session_state.start_time
    time_left = max(0, THOI_GIAN_THI - int(time_elapsed))
    
    # KHI HẾT GIỜ HOẶC HẾT CÂU HỎI
    if time_left == 0 or st.session_state.current_q >= len(st.session_state.questions):
        st.session_state.is_playing = False
        st.success("Tích tắc tích tắc... Trận đấu kết thúc! 🏁")
        if time_left == 0:
            st.error("⏰ Hết thời gian!")
        
        st.balloons()
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background-color: #1E1E1E; border-radius: 10px; margin-bottom: 20px;'>
            <h3>Tổng điểm của bạn</h3>
            <h1 style='color: #FFD700; font-size: 50px;'>{st.session_state.score} 🏆</h1>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Chơi lại ván khác", use_container_width=True):
            fetch_questions()
            st.rerun()
            
    # KHI ĐANG TRONG TRẬN ĐẤU
    else:
        q = st.session_state.questions[st.session_state.current_q]
        
        # HIỂN THỊ ĐỒNG HỒ VÀ TIẾN ĐỘ
        col1, col2, col3 = st.columns(3)
        col1.metric("Tiến độ", f"Câu {st.session_state.current_q + 1} / {len(st.session_state.questions)}")
        col2.metric("Điểm hiện tại", f"{st.session_state.score} 🏆")
        col3.metric("⏳ Thời gian còn", f"{time_left} s")
        
        # Thanh tiến độ thời gian (trượt dần về 0)
        progress_val = time_left / THOI_GIAN_THI
        st.progress(progress_val)
        
        # Tự động refresh lại trang mỗi giây để đồng hồ chạy
        time.sleep(1)
        st.rerun() 
        
        # NỘI DUNG CÂU HỎI
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
