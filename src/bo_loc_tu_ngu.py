# Tên file: bo_loc_tu_ngu.py
import re

def cham_diem_vi_pham(text):
    """
    Công cụ kiểm duyệt dùng chung cho toàn bộ dự án.
    Chấm điểm từ 0 - 100 dựa trên từ ngữ vi phạm.
    """
    if not text:
        return {"diem_vi_pham": 0, "nhan_danh_gia": "An Toàn", "hanh_dong_de_xuat": "Cho phép đăng", "chi_tiet": {}}

    bo_tu_dien = {
        "đm": 50, "địt": 50, "cút": 50, "chó": 50, "ngu": 50, "cặc": 50, "lồn": 50,
        "vcl": 30, "vl": 30, "vãi": 30, "cmn": 30, "đậu xanh": 30, "mẹ bà": 30,
        "mày": 15, "tao": 15, "thằng": 15, "con kia": 15, "tụi bay": 15
    }

    diem_tong = 0
    chi_tiet_loi = {} 
    text_lower = text.lower()

    for tu, diem_phat in bo_tu_dien.items():
        matches = re.findall(rf'\b{tu}\b', text_lower)
        so_lan_lap_lai = len(matches)
        
        if so_lan_lap_lai > 0:
            diem_cong_them = so_lan_lap_lai * diem_phat
            diem_tong += diem_cong_them
            chi_tiet_loi[tu] = f"{so_lan_lap_lai} lần (Phạt {diem_cong_them}đ)"

    diem_tong = min(100, diem_tong)

    if diem_tong == 0:
        nhan = "An Toàn"
        hanh_dong = "Cho phép đăng"
    elif diem_tong <= 30:
        nhan = "Cảnh Cáo Nhẹ"
        hanh_dong = "Nhắc nhở điều chỉnh ngôn từ"
    elif diem_tong <= 70:
        nhan = "Vi Phạm Nặng"
        hanh_dong = "Ẩn bài viết, thông báo quản trị"
    else:
        nhan = "Rất Độc Hại"
        hanh_dong = "Cấm đăng, khóa tài khoản"

    return {
        "diem_vi_pham": diem_tong,
        "nhan_danh_gia": nhan,
        "hanh_dong_de_xuat": hanh_dong,
        "chi_tiet": chi_tiet_loi
    }
