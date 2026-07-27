def determine_action(severity: int, category: str, strikes: int = 0) -> str:
    """Quyết định hình phạt cuối cùng"""
    
    # Cộng dồn điểm nếu học sinh đã có tiền sử vi phạm (strikes)
    adjusted_severity = severity + (strikes * 15)
    if adjusted_severity > 100:
        adjusted_severity = 100

    # Khung hình phạt
    if adjusted_severity < 20:
        return "allow"
    elif adjusted_severity < 40:
        return "review"
    elif adjusted_severity < 60:
        return "remove" if category in ["spam", "pornography"] else "warn"
    elif adjusted_severity < 80:
        return "ban_temp"
    else:
        return "ban_perm"

def determine_label(action: str) -> str:
    """Đổi hành động ra nhãn dễ nhìn"""
    if action == "allow": return "SAFE"
    if action == "review": return "SUSPICIOUS"
    return "VIOLATION"
