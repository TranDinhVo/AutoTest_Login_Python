# AutoTest_Login_Python — Kiểm thử đăng nhập Văn phòng điện tử UTC

Dự án kiểm thử tự động chức năng **Đăng nhập** của trang
[vanphongdientu.utc.edu.vn](https://vanphongdientu.utc.edu.vn/) bằng
**Python + Selenium + pytest**, kèm **bảng test case Excel**.

## ⚠️ Nguyên tắc an toàn (đọc trước khi chạy)

- Automation chạy mặc định trên **bản MOCK login đóng gói sẵn** trong
  `mock_login/` (chạy offline, **không đụng server thật của trường**).
- Test **SQL Injection / XSS** là kiểm thử **input-validation**: xác minh trang
  xử lý payload như chuỗi, **không bị bypass đăng nhập, không thực thi mã**.
  Đây là kiểm thử phòng thủ, không phải tấn công.
- Có **chốt an toàn**: test bảo mật chỉ chạy khi mục tiêu nằm trong
  `security_allowed_hosts` (mock/localhost/demo). Nếu trỏ vào server thật,
  các test bảo mật **tự động bị bỏ qua (skip)**.
- **DoS/DDoS**: dự án **không cung cấp và không chạy** script tấn công. Mục này
  chỉ được ghi nhận trong bảng test case như **rủi ro + biện pháp phòng thủ**.
  Muốn đánh giá tải thì dùng JMeter trên **môi trường staging được cấp phép**.

## Cấu trúc

```
AutoTest_Login_Python/
├── config.ini                 # cấu hình: mục tiêu test, locator, chốt an toàn
├── conftest.py                # fixtures pytest (driver, config, login_page)
├── requirements.txt
├── pytest.ini
├── mock_login/                # trang login giả lập (login.html, logged-in...)
├── pages/login_page.py        # Page Object
├── utils/config_loader.py     # đọc config.ini
├── tests/                     # các test, mỗi test case = 1 hàm test
│   ├── test_login_functional.py
│   ├── test_login_security.py
│   └── test_login_robustness.py
└── testcases/
    └── TestCase_DangNhap_VanPhongDienTu.xlsx
```

## Cài đặt

```powershell
# 1. (khuyến nghị) tạo môi trường ảo
py -m venv .venv
.venv\Scripts\activate

# 2. cài thư viện
pip install -r requirements.txt
```

> Selenium 4 tự tải driver qua Selenium Manager — không cần tải chromedriver thủ công.
> Máy cần sẵn **Google Chrome** (hoặc đổi `browser = edge` trong `config.ini`).

## Chạy test

```powershell
pytest                      # chạy tất cả
pytest -m functional        # chỉ test chức năng
pytest -m security          # chỉ test bảo mật (SQLi, XSS)
pytest -m robustness        # chỉ test độ bền
pytest --html=report.html   # xuất báo cáo HTML
```

Xem trình duyệt chạy: đổi `headless = false` trong `config.ini`.

## Ánh xạ test case ↔ code

| Bảng Excel (sheet) | File test |
|---|---|
| ChucNang (TC01–TC10) | `tests/test_login_functional.py` |
| BaoMat (SEC01–SEC07) | `tests/test_login_security.py` |
| DoBen (ROB01–ROB03)  | `tests/test_login_robustness.py` |
