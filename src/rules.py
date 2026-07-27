import re
from typing import Dict, Any, Tuple

# Từ điển từ khóa mẫu (có thể tự do thêm bớt cho phù hợp học sinh)
VIOLATION_KEYWORDS = {
    "violence": ["giết", "đâm", "chém", "đập phá", "bom", "khủng bố"],
    "doxxing": ["cccd", "cmnd", "địa chỉ nhà", "số điện thoại của"],
    "insult": ["ngu xuẩn", "súc vật", "thằng chó", "con đĩ", "cặn bã", "ngu dốt"],
    "spam": ["nhấp vào link", "kiếm tiền tại nhà", "nổ hũ", "đăng ký ngay để nhận"],
    "pornography": ["phim heo", "lộ clip", "ảnh nóng", "18+"]
}

def analyze_rules(text: str) -> Tuple[int, str, str]:
    """
    Quét văn bản dựa trên rules. 
    Trả về: (severity_score, category, excerpt)
    """
    text_lower = text.lower()
    max_severity = 0
    detected_category = "none"
    excerpt = ""

    for category, keywords in VIOLATION_KEYWORDS.items():
        for word in keywords:
            if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
                # Chấm điểm theo mức độ nghiêm trọng
                if category in ["violence", "doxxing", "pornography"]:
                    score = 90
                elif category in ["insult"]:
                    score = 60
                elif category in ["spam"]:
                    score = 50
                else:
                    score = 20
                
                if score > max_severity:
                    max_severity = score
                    detected_category = category
                    # Lấy một đoạn văn bản ngắn xung quanh từ khóa lỗi
                    idx = text_lower.find(word)
                    start = max(0, idx - 20)
                    end = min(len(text), idx + len(word) + 20)
                    excerpt = text[start:end]

    return max_severity, detected_category, excerpt
