import streamlit as st
import streamlit as st

# Thiết lập cấu hình trang (Tùy chọn, để tab trình duyệt trông chuyên nghiệp hơn)
st.set_page_config(
    page_title="Trang Chủ - THCS Sông Ray EVN", # Tiêu đề tab trình duyệt
    page_icon="🏫",                             # Biểu tượng tab trình duyệt
    layout="wide"                              # Chế độ hiển thị rộng (Tùy chọn)
)

# Hiển thị hình ảnh banner
# GIẢ SỬ: Fen lưu bức ảnh trên GitHub với tên là 'banner_thcs_song_ray.png' 
# và đặt nó cùng thư mục với file app.py này.
st.image("banner_thcs_song_ray.png", use_container_width=True)

# Thêm một chút nội dung chào mừng bên dưới cho đẹp
st.title("👋 Chào mừng đến với Diễn Đàn Học Tập THCS Sông Ray")
st.write("Dự án được phát triển bởi **Phan Lê Dũng** và **Bùi Khang An** (EVN).")
st.markdown("---")
st.write("Nơi trao đổi kiến thức và giải đáp thắc mắc về môn Địa lý và các môn học khác.")
# Cấu hình giao diện Trang chủ
st.set_page_config(page_title="Cổng Thông Tin Học Tập", page_icon="🏫", layout="centered")

st.title("🎓 Cổng Thông Tin & Diễn Đàn Học Tập THCS")

st.write("Chào mừng bạn đến với hệ thống hỗ trợ học tập trực tuyến tích hợp AI!")

st.divider()

st.subheader("📌 Vui lòng chọn tính năng:")

# Các nút dẫn vào các trang chức năng
st.page_link("pages/0_Tai_Khoan.py", label="👤 Đăng Nhập / Đăng Ký", use_container_width=True)
st.page_link("pages/1_Dien_Dan.py", label="💬 Vào Diễn Đàn Thảo Luận", use_container_width=True)

# 2 nút này tạm ẩn vì bro chưa làm, chừng nào làm thì xóa dấu # đi nhé
# st.page_link("pages/2_Bang_Xep_Hang.py", label="🏆 Xem Bảng Xếp Hạng", use_container_width=True)
# st.page_link("pages/3_Trac_Nghiem_AI.py", label="📝 Làm Trắc Nghiệm", use_container_width=True)

st.page_link("pages/4_Kiem_Duyet_Admin.py", label="🛡️ Quản Trị Hệ Thống (Admin)", use_container_width=True)
