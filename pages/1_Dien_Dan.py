import streamlit as st
import requests
import json
from google import genai

# 1. Cấu hình trang
st.set_page_config(page_title="Diễn Đàn Thảo Luận AI", page_icon="💬", layout="wide")

# 🔴 DÁN LINK APPS SCRIPT CỦA BRO VÀO ĐÂY:
GSHEETS_URL = "https://script.google.com/macros/s/AKfycby0X2IWEgzp-MmGSHSaUGVafRGMuP5pQZ4GS0MrldMrJ2sHDugNaP62vQt89JzPbIC4/exec"

st.title("💬 Diễn Đàn & AI Kiểm Duyệt Nâng Cao")
st.caption("AI phân tích chuyên sâu nội dung dựa trên tiêu chuẩn cộng đồng")
st.page_link("app.py", label="🏠 Quay về Trang Chủ", use_container_width=False)
st.divider()

# Sidebar Cấu hình
st.sidebar.header("⚙️ Cấu hình Hệ thống")
api_key = st.sidebar.text_input("🔑 Nhập Gemini API Key:", type="password").strip()
selected_model = st.sidebar.selectbox("🤖 Mô hình AI:", ["gemini-2.0-flash", "gemini-2.0-flash-lite"])
bypass_ai = st.sidebar.checkbox("🛠️ Bật chế độ Test (Tắt AI)", value=False)

if st.sidebar.button("🔄 Tải lại diễn đàn"):
    st.cache_data.clear()
    st.rerun()

# Hàm tối ưu: Lấy bài viết
@st.cache_data(ttl=5, show_spinner=False)
def fetch_posts(url):
    if not url or "DÁN_LINK" in url: return []
    try:
        res = requests.get(url, timeout=5)
        return res.json() if res.status_code == 200 else []
    except Exception: return []

# Hàm tối ưu: Gửi dữ liệu
def send_to_sheets(payload):
    try:
        requests.post(GSHEETS_URL, json=payload, timeout=5)
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Lỗi lưu CSDL: {e}")
        return False

# ----------------- PROMPT KIỂM DUYỆT CỦA BRO -----------------
SYSTEM_PROMPT = """
Bạn là một module lọc nội dung tự động cho diễn đàn dự án. Nhiệm vụ: phân loại và quyết định hành động đối với mỗi bài thảo luận hoặc bình luận mới dựa trên nội dung văn bản.
Yêu cầu phân loại:
Xác định xem văn bản có chứa bất kỳ dạng sau không: xúc phạm cá nhân (insult), ngôn từ thù ghét (hate speech), kêu gọi bạo lực (violence incitement), quấy rối/lăng mạ (harassment), đe dọa, tiết lộ thông tin nhạy cảm (doxing), ngôn từ khiêu dâm không phù hợp, spam quảng cáo.
Bỏ qua (không đánh là vi phạm) khi nội dung là trích dẫn học thuật, thảo luận chính trị/giải thích, hoặc báo cáo hành vi mang tính mô tả, nhưng vẫn lưu ý nếu văn bản thể hiện ủng hộ nội dung vi phạm.

Quy tắc tỷ lệ/ứng xử:
- Nếu phát hiện nội dung kêu gọi bạo lực, đe dọa trực tiếp, hoặc doxing => hành động: ban_permanent.
- Nếu nhiều câu xúc phạm nặng, lặp lại nhiều lần => hành động: ban_temporary nếu mức độ trung bình; ban_permanent nếu cực đoan.
- Nếu xúc phạm nhẹ hoặc 1 lần => hành động: warn và ẩn bài (remove_post).
- Nếu chỉ spam hoặc quảng cáo => hành động: remove_post, warn, và nếu lặp lại => ban_temporary.
- Nếu nội dung gây tranh cãi nhưng không xúc phạm trực tiếp => để công khai nhưng gắn nhãn "có tranh cãi" (quy vào allow nhưng score thấp).

Đầu ra bắt buộc: Trả về DUY NHẤT một chuỗi JSON hợp lệ, KHÔNG kèm giải thích.
Cấu trúc dạng:
{
  "decision": "<action>",
  "category": "<violation_category>",
  "severity_score": <0-100>,
  "reason_summary": "<tóm tắt lý do ngắn gọn>",
  "examples": ["<trích đoạn 1>"],
  "recommended_penalty": {"type": "<penalty_type>", "duration_days": <số>}
}
(Trong đó action: allow, remove_post, warn, ban_temporary, ban_permanent, flag_for_review)
"""
# -------------------------------------------------------------

# Khung Đăng bài
st.subheader("✍️ Đăng bài thảo luận mới")
col1, col2 = st.columns([1, 2])

with col1:
    subject = st.selectbox("📚 Môn học:", ["Toán học", "Ngữ văn", "Tiếng Anh", "Vật lý", "Khác"])
    # Giả lập thông tin user để test AI
    sim_age = st.number_input("Tuổi của bạn (để test AI):", min_value=9, max_value=60, value=15)
    sim_strikes = st.number_input("Số lần vi phạm trước đó:", min_value=0, max_value=10, value=0)

with col2:
    user_input = st.text_area("📝 Nội dung thảo luận:", height=130)

if st.button("🚀 Đăng bài ngay", type="primary", use_container_width=True):
    if not user_input.strip():
        st.warning("Vui lòng nhập nội dung!")
    elif bypass_ai:
        if send_to_sheets({"action": "add_post", "subject": subject, "content": user_input}):
            st.success("✅ Đã đăng thành công (Chế độ bỏ qua AI)!")
            st.rerun()
    else:
        if not api_key:
            st.error("⚠️ Cần nhập Gemini API Key ở thanh bên trái!")
        else:
            with st.spinner("🤖 Trí tuệ nhân tạo đang phân tích lớp lang nội dung..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    # Ghép data người dùng vào format JSON như bro yêu cầu
                    user_data_input = {
                        "post_text": user_input.strip(),
                        "user_id": "student_001",
                        "user_age": sim_age,
                        "user_history": {"strikes": sim_strikes}
                    }
                    
                    final_prompt = f"{SYSTEM_PROMPT}\n\nĐầu vào:\n{json.dumps(user_data_input, ensure_ascii=False)}"
                    
                    res = client.models.generate_content(model=selected_model, contents=final_prompt)
                    
                    # Bóc tách JSON từ phản hồi của AI (loại bỏ ký tự markdown nếu có)
                    raw_text = res.text.replace("```json", "").replace("```", "").strip()
                    ai_result = json.loads(raw_text)
                    
                    decision = ai_result.get("decision", "")
                    
                    # Hiển thị bảng phân tích của AI cho Admin/Học sinh xem
                    with st.expander("📊 Xem chi tiết kiểm duyệt của AI", expanded=(decision != "allow")):
                        st.json(ai_result)
                    
                    # Xử lý Logic dựa trên "decision" của AI
                    if decision == "allow":
                        if send_to_sheets({"action": "add_post", "subject": subject, "content": user_input}):
                            st.success("✅ Bài viết an toàn! Đã đăng lên diễn đàn.")
                            st.rerun()
                    else:
                        st.error(f"❌ Bài viết bị từ chối! Hành động AI đề xuất: **{decision.upper()}**")
                        st.warning(f"**Lý do:** {ai_result.get('reason_summary', 'Vi phạm tiêu chuẩn cộng đồng')}")
                        st.info(f"**Mức độ nghiêm trọng:** {ai_result.get('severity_score')}/100")
                        
                except Exception as e:
                    st.error(f"Lỗi phân tích AI hoặc cấu trúc JSON: {e}")

st.divider()

# Danh sách bài viết
posts = fetch_posts(GSHEETS_URL)
st.subheader(f"📌 Dòng thời gian ({len(posts)} bài viết)")

if not posts:
    st.info("Chưa có bài đăng nào.")
else:
    for idx, post in enumerate(posts):
        with st.container(border=True):
            st.markdown(f"**[{post.get('subject', 'Khác')}]**")
            st.write(post.get('content', ''))
            
            comments = post.get('comments', [])
            if comments:
                st.caption("💬 Các bình luận:")
                for c in comments:
                    st.info(f"👉 {c}")
            
            with st.expander("💬 Viết câu trả lời"):
                reply = st.text_input("Nội dung:", key=f"rep_{post.get('id', idx)}")
                if st.button("Gửi bình luận", key=f"btn_{post.get('id', idx)}"):
                    if reply.strip():
                        with st.spinner("⚡ Đang gửi..."):
                            send_to_sheets({"action": "add_comment", "post_id": post.get('id'), "comment": reply.strip()})
                            st.success("Đã trả lời!")
                            st.rerun()
