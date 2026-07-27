import requests

def analyze_with_ai(text: str, api_key: str, model_name: str = "omni-moderation-latest") -> dict:
    """
    Gửi văn bản tới OpenAI Moderation API (Miễn phí 100%).
    Tự động chuyển đổi kết quả OpenAI về cấu trúc JSON chuẩn của hệ thống.
    """
    if not api_key or not text.strip():
        return None

    url = "https://api.openai.com/v1/moderations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key.strip()}"
    }
    payload = {
        "model": model_name,
        "input": text.strip()
    }

    try:
        # Gọi API của OpenAI bằng thư viện requests có sẵn
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code != 200:
            print(f"[OpenAI Error] Mã lỗi: {response.status_code} - {response.text}")
            return None

        data = response.json()
        results = data.get("results", [])[0]

        flagged = results.get("flagged", False)
        category_scores = results.get("category_scores", {})

        # Tìm loại vi phạm có điểm số cao nhất từ OpenAI
        max_cat = "none"
        max_score = 0.0

        for cat, score in category_scores.items():
            if score > max_score:
                max_score = score
                max_cat = cat

        # Quy đổi điểm OpenAI (từ 0.0 - 1.0) sang thang điểm hệ thống (0 - 100)
        severity = int(max_score * 100)

        # Ánh xạ (Map) loại vi phạm của OpenAI sang danh mục của hệ thống
        cat_mapping = {
            "hate": "hate_speech",
            "hate/threatening": "hate_speech",
            "harassment": "harassment",
            "harassment/threatening": "harassment",
            "self-harm": "violence",
            "sexual": "pornography",
            "sexual/minors": "pornography",
            "violence": "violence",
            "violence/graphic": "violence"
        }

        mapped_category = cat_mapping.get(max_cat, "insult" if flagged else "none")

        # Nếu OpenAI đánh dấu vi phạm (flagged) nhưng điểm hơi thấp, tự nâng lên 60 điểm để xử phạt
        if flagged and severity < 60:
            severity = 60

        reason = f"OpenAI Moderation phát hiện vi phạm nhóm: '{max_cat}'" if flagged else "Nội dung an toàn theo đánh giá của OpenAI."

        # Trả về Dictionary đúng chuẩn Pydantic Schema mà hệ thống đang dùng
        return {
            "severity": severity,
            "category": mapped_category,
            "reason": reason,
            "excerpt": text if flagged else ""
        }

    except Exception as e:
        print(f"[OpenAI Client Exception] Lỗi: {e}")
        return None
