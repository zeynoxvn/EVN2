import json
from google import genai

SYSTEM_PROMPT = """
Bạn là hệ thống kiểm duyệt nội dung. Hãy phân tích văn bản và trả về JSON chuẩn xác.
Các loại vi phạm (category): insult, hate_speech, violence, harassment, doxxing, pornography, spam, none.
Điểm nghiêm trọng (severity): 0 - 100.
CHỈ TRẢ VỀ JSON, không kèm markdown hay giải thích.
Cấu trúc JSON bắt buộc:
{
  "severity": <int>,
  "category": "<chuỗi>",
  "reason": "<lý do ngắn>",
  "excerpt": "<trích đoạn vi phạm nếu có>"
}
"""

def analyze_with_ai(text: str, api_key: str, model_name: str = "gemini-2.0-flash-lite") -> dict:
    """Gọi Gemini AI để phân tích sắc thái ngữ cảnh"""
    try:
        client = genai.Client(api_key=api_key)
        prompt = f"{SYSTEM_PROMPT}\n\nVăn bản cần kiểm duyệt:\n{text}"
        
        response = client.models.generate_content(
            model=model_name, 
            contents=prompt
        )
        
        # Làm sạch chuỗi JSON lỡ AI có thêm dấu markdown ```json
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        result = json.loads(raw_text.strip())
        return result
    except Exception as e:
        print(f"AI API Error: {e}")
        return None
