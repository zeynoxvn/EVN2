from .rules import analyze_rules
from .ai_client import analyze_with_ai
from .decision_engine import determine_action, determine_label
from .schemas import ModerationResult

def moderate_content(text: str, api_key: str = None, strikes: int = 0, force_ai: bool = False) -> ModerationResult:
    """
    Luồng xử lý chính:
    1. Check rule-based trước để lọc từ bậy rõ ràng.
    2. Nếu rule-based chắc chắn vi phạm nặng (severity >= 80), phạt luôn không tốn tiền gọi AI.
    3. Nếu kết quả mơ hồ (0 < severity < 80) hoặc ép dùng AI (force_ai), mới gọi Google Gemini.
    """
    used_ai = False
    
    # 1. Bộ lọc tĩnh
    severity, category, excerpt = analyze_rules(text)
    reason = "Phát hiện từ khóa vi phạm (Hệ thống tự động)."
    
    # 2. Phân tích AI dự phòng
    if api_key and (force_ai or (0 < severity < 80)):
        ai_result = analyze_with_ai(text, api_key)
        if ai_result:
            used_ai = True
            severity = ai_result.get("severity", severity)
            category = ai_result.get("category", category)
            reason = ai_result.get("reason", "Phân tích ngữ cảnh bởi AI.")
            excerpt = ai_result.get("excerpt", excerpt)
            
    # Xử lý trường hợp văn bản an toàn
    if severity == 0 and not used_ai:
        category = "none"
        reason = "Nội dung an toàn, không chứa từ khóa vi phạm."

    # 3. Ra quyết định cuối cùng
    action = determine_action(severity, category, strikes)
    label = determine_label(action)

    return ModerationResult(
        label=label,
        severity=severity,
        category=category,
        action=action,
        reason=reason,
        excerpt=excerpt,
        used_ai=used_ai
    )
