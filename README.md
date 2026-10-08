# AutoTest_Login_Python — Kiểm thử đăng nhập Văn phòng điện tử UTC

Dự án kiểm thử tự động chức năng **Đăng nhập** của trang
[vanphongdientu.utc.edu.vn](https://vanphongdientu.utc.edu.vn/) bằng
**Python + Selenium + pytest**, kèm **bảng test case Excel**.

## Nguyên tắc an toàn (đọc trước khi chạy)

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

Theo mô hình **Page Object Model (POM)** chuẩn (buổi 8): tách `base/`, `pages/`, `tests/`.

```
AutoTest_Login_Python/
├── config.ini                 # cấu hình: mục tiêu test, chốt an toàn
├── requirements.txt
├── pytest.ini                 # cấu hình pytest + tự sinh report vào reports/
├── base/                      # hạ tầng test
│   └── base_test.py           # BaseTest: khởi tạo WebDriver + timeout (BeforeEach/AfterEach)
├── pages/                     # CÁC PAGE OBJECT
│   ├── base_page.py           # BasePage: thao tác chung wait/click/type/get_text
│   ├── login_page.py          # LoginPage: form đăng nhập (locator private)
│   └── dashboard_page.py      # DashboardPage: trang chủ sau đăng nhập
├── tests/                     # CÁC TEST (mỗi test case = 1 method)
│   ├── test_login_functional.py
│   ├── test_login_security.py
│   └── test_login_robustness.py
├── utils/config_loader.py     # đọc config.ini
├── mock_login/                # trang login giả lập (login.html, logged-in...)
├── reports/                   # báo cáo tự sinh (report.html + junit.xml) — như surefire-reports
└── testcases/
    └── TestCase_DangNhap_VanPhongDienTu.xlsx
```

**Quy ước POM:** locator để private trong page, page không chứa assertion, method
nghiệp vụ trả về trang kế tiếp (fluent), dùng Explicit Wait, không `sleep`.

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
pytest                      # chạy tất cả (tự sinh report)
pytest -m functional        # chỉ test chức năng
pytest -m security          # chỉ test bảo mật (SQLi, XSS)
pytest -m robustness        # chỉ test độ bền
```

Xem trình duyệt chạy: đổi `headless = false` trong `config.ini`.

## Báo cáo test (giống surefire-reports bên Java)

Mỗi lần chạy `pytest` tự sinh báo cáo vào thư mục `reports/`:

- `reports/report.html` — báo cáo **HTML** (pytest-html), mở bằng trình duyệt,
  xem pass/fail từng test, thời gian chạy, log lỗi.
- `reports/junit.xml` — báo cáo **JUnit XML** (giống `TEST-*.xml` của Surefire),
  để CI/công cụ khác đọc.

Trên GitHub Actions, báo cáo được lưu làm *artifact* `test-report` (tải về ở tab Actions).

## Ánh xạ test case - code

| Bảng Excel (sheet) | File test |
|---|---|
| ChucNang (TC01–TC10) | `tests/test_login_functional.py` |
| BaoMat (SEC01–SEC15) | `tests/test_login_security.py` |
| DoBen (ROB01–ROB03)  | `tests/test_login_robustness.py` |
