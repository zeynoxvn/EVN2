import re
from typing import Tuple

# Từ điển từ khóa vi phạm (Bổ sung đầy đủ từ bậy Tiếng Việt & từ nhạy cảm)
VIOLATION_KEYWORDS = {
    "insult": [
        "địt", "dit", "địt mẹ", "địt má", "dịt", "con cặc", "cặc", "cak", "lồn", "lon", "vãi lồn", "vãi l",
        "đm", "dm", "dmm", "dcm", "clm", "đclm", "vcl", "vl", "đmẹ", "dme",
        "súc vật", "con đĩ", "thằng chó", "cặn bã", "ngu dốt", "đồ chó", "óc chó", "thằng lồn", "con điếm"
    ],
    "political_insult": [
        "lăng mạ", "lăng mạ lãnh đạo", "xúc phạm lãnh đạo", "chống phá nhà nước", "phản động", 
        "xúc phạm bác", "xúc phạm anh hùng", "xuyên tạc lịch sử", "đu càng", "ba sọc", "3 sọc"
    ],
    "violence": ["giết", "đâm", "chém", "đập phá", "bom", "khủng bố", "súng đạn", "cắt cổ"],
    "doxxing": ["cccd", "cmnd", "địa chỉ nhà", "số điện thoại của"],
    "spam": ["nhấp vào link", "kiếm tiền tại nhà", "nổ hũ", "đăng ký ngay để nhận", "tài xỉu", "lô đề"],
    "pornography": ["phim heo", "lộ clip", "ảnh nóng", "18+", "thủ dâm", "phim jav", "xvideos"]
}

def analyze_rules(text: str) -> Tuple[int, str, str]:
    """
    Quét văn bản Tiếng Việt dựa trên bộ từ khóa.
    Sử dụng thuật toán tìm kiếm chuỗi con (substring) để nhận diện chính xác Tiếng Việt có dấu/không dấu.
    """
    text_lower = text.lower()
    max_severity = 0
    detected_category = "none"
    excerpt = ""

    for category, keywords in VIOLATION_KEYWORDS.items():
        for word in keywords:
            # Dùng so sánh chuỗi trực tiếp (in) để bắt dính 100% tiếng Việt
            if word in text_lower:
                # Chấm điểm phạt cực nặng cho các hành vi này
                if category in ["violence", "doxxing", "pornography", "political_insult"]:
                    score = 90
                elif category in ["insult"]:
                    score = 85
                elif category in ["spam"]:
                    score = 60
                else:
                    score = 20
                
                # Cập nhật vi phạm nặng nhất nếu trong câu có nhiều lỗi
                if score > max_severity:
                    max_severity = score
                    detected_category = category
                    
                    # Cắt 1 đoạn văn bản (trước và sau từ vi phạm 15 ký tự) để làm bằng chứng
                    idx = text_lower.find(word)
                    start = max(0, idx - 15)
                    end = min(len(text), idx + len(word) + 15)
                    excerpt = "..." + text[start:end] + "..."

    return max_severity, detected_category, excerpt
