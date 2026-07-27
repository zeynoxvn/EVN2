import json
from google import genai

SYSTEM_PROMPT = """
Bạn là hệ thống kiểm duyệt nội dung tự động. Hãy phân tích ngữ cảnh văn bản và trả về định dạng JSON chuẩn xác.
Các loại vi phạm (category): insult, hate_speech, violence, harassment, doxxing, pornography, spam, none.
Điểm nghiêm trọng (severity): từ 0 (hoàn toàn an toàn) đến 100 (cực kỳ nghiêm trọng).

CHỈ TRẢ VỀ CHUỖI JSON, KHÔNG KÈM VĂN BẢN GIẢI THÍCH HOẶC MARKDOWN.
Cấu trúc JSON bắt buộc:
{
  "severity": <số nguyên từ 0-100>,
  "category": "<chuỗi loại vi phạm>",
  "reason": "<lý do ngắn gọn 1 câu>",
  "excerpt": "<trích đoạn văn bản vi phạm nếu có, nếu không có thì để rỗng ''>"
}
"""

def analyze_with_ai(text: str, api_key: str, model_name: str = "gemini-1.5-flash-8b") -> dict:
    """
    Gọi Google Gemini API để phân tích ngữ cảnh bài viết.
    Tự động bắt lỗi API và bóc tách định dạng JSON trả về.
    """
    if not api_key or not text.strip():
        return None

    try:
        # Khởi tạo Client Gemini với API Key người dùng cung cấp
        client = genai.Client(api_key=api_key)
        
        prompt = f"{SYSTEM_PROMPT}\n\nVăn bản cần kiểm duyệt:\n'{text}'"
        
        # Gọi mô hình AI
        response = client.models.generate_content(
            model=model_name, 
            contents=prompt
        )
        
        if not response or not response.text:
            return None

        # Bóc tách và dọn dẹp chuỗi JSON nếu AI vô tình trả về thêm ```json ... ```
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:]
            
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        raw_text = raw_text.strip()
            
        # Parse chuỗi thành Dictionary Python
        result = json.loads(raw_text)
        return result

    except json.JSONDecodeError as e:
        print(f"[AI Client Error] Không thể parse JSON từ phản hồi AI: {e}")
        return None
    except Exception as e:
        print(f"[AI Client Error] Lỗi gọi API Gemini: {e}")
        return None
