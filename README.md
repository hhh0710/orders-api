# Mock Orders API

Service dữ liệu đơn hàng cho dự án `customer-portal`. Chỉ dùng dữ liệu giả và lắng nghe tại `127.0.0.1`; đây là fixture để kiểm thử whitebox, không phải ứng dụng production.

Yêu cầu Python 3.10+, không cần cài thư viện.

```powershell
python app.py
```

Cổng mặc định: `8766`. Có thể dùng `--port 9006`.

- `GET /orders`: danh sách đơn hàng của khách hàng hiện tại.
- `GET /orders/{id}`: chi tiết một đơn hàng.
- Context khách hàng do portal chuyển qua header `X-Customer-ID`.
- Dữ liệu trong bộ nhớ: Alice có đơn `1001`, `1003`; Bob có đơn `1002`.

Trong kiến trúc mock, service này là API nội bộ, tin context do portal chuyển đến. Yêu cầu sản phẩm: một khách hàng chỉ được xem đơn hàng của chính mình qua portal. Không lưu dữ liệu hay truy cập dịch vụ bên ngoài.
