import streamlit as st
import requests

st.set_page_config(page_title="Sàn Đấu Toán Học", page_icon="⚔️")

# ==========================================
# 1. NÚT QUAY LẠI (LÚC NÀO CŨNG HIỆN)
# ==========================================
st.page_link("app.py", label="🏠 Quay lại Trang chủ", icon="⬅️")
st.markdown("---") # Kẻ một đường ngang cho tách biệt

# --- ĐIỀN LINK API CỦA FEN VÀO ĐÂY ---
API_URL = "https://script.google.com/macros/s/AKfycbzV0KqHng6Edeb8LupXLSY84M_v4VnenGHenVWj_d7pvzVlsq2KWwh7dN-xwOSP33oh/exec" 

# ==========================================
# 2. KHÓA CỬA SÀN ĐẤU (NẾU CHƯA ĐĂNG NHẬP)
# ==========================================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Khu vực hạn chế: Bạn chưa báo danh!")
    st.info("Vui lòng bấm nút 'Quay lại Trang chủ' ở trên hoặc chọn trang Đăng Nhập bên menu trái để ghi danh nhé.")
    st.stop() # Lệnh này sẽ chặn đứng, không cho hiện câu hỏi bên dưới

# ==========================================
# 3. SÀN ĐẤU (CHỈ HIỆN KHI ĐÃ ĐĂNG NHẬP)
# ==========================================
st.title("⚔️ Sàn Đấu Toán Học")
st.markdown("Chào mừng các cao thủ đến với đấu trường trí tuệ!")

# KHỞI TẠO BỘ NHỚ TẠM CHO TRẬN ĐẤU
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "is_playing" not in st.session_state:
    st.session_state.is_playing = False

# HÀM LẤY ĐỀ TỪ GOOGLE SHEETS
def fetch_questions():
    with st.spinner("Đang xáo trộn bộ câu hỏi từ ngân hàng đề..."):
        try:
            payload = {"action": "get_match_questions", "limit": 5}
            response = requests.post(API_URL, json=payload).json()
            
            if response.get("status") == "success":
                st.session_state.questions = response["data"]
                st.session_state.current_q = 0
                st.session_state.score = 0
                st.session_state.is_playing = True
                st.rerun() 
            else:
                st.error(f"Lỗi từ máy chủ: {response.get('message')}")
        except Exception as e:
            st.error(f"Không thể kết nối API. Vui lòng kiểm tra lại đường link: {e}")

# HÀM CHẤM ĐIỂM
def check_answer(selected_option, correct_answer):
    if selected_option == correct_answer:
        st.session_state.score += 10
        st.toast("Chính xác! +10 điểm 🎉", icon="✅")
    else:
        st.toast(f"Sai rồi! Đáp án đúng là {correct_answer} ❌", icon="🚨")
    st.session_state.current_q += 1

# GIAO DIỆN THI ĐẤU
if not st.session_state.is_playing:
    st.info("Nhấn nút bên dưới để bắt đầu bốc 5 câu hỏi ngẫu nhiên và tính giờ!")
    if st.button("🚀 BẮT ĐẦU THI ĐẤU", use_container_width=True, type="primary"):
        fetch_questions()
else:
    if st.session_state.current_q < len(st.session_state.questions):
        q = st.session_state.questions[st.session_state.current_q]
        col1, col2 = st.columns(2)
        col1.metric("Tiến độ", f"Câu {st.session_state.current_q + 1} / {len(st.session_state.questions)}")
        col2.metric("Điểm hiện tại", f"{st.session_state.score} 🏆")
        
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
    else:
        st.success("Tích tắc tích tắc... Trận đấu kết thúc! 🏁")
        st.balloons()
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background-color: #1E1E1E; border-radius: 10px; margin-bottom: 20px;'>
            <h3>Tổng điểm của bạn</h3>
            <h1 style='color: #FFD700; font-size: 50px;'>{st.session_state.score} 🏆</h1>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Chơi lại ván khác", use_container_width=True):
            st.session_state.is_playing = False
            st.rerun()
