# 🍷 ML API - Wine Quality & Customer Segmentation

API Flask dự đoán chất lượng rượu vang và phân cụm khách hàng.

---

## 📌 SƠ ĐỒ HOẠT ĐỘNG

```
┌────────────────────────────────────────────────────────────┐
│                     MÔ HÌNH HOẠT ĐỘNG                      │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1️⃣ Flask API Server (Port 8080)                          │
│     ├─ Serve HTML/CSS/JS                                  │
│     ├─ Xử lý ML predictions                               │
│     └─ Load 3 models (.joblib)                            │
│                                                            │
│  2️⃣ Browser (Client)                                      │
│     ├─ Tải giao diện web                                  │
│     ├─ JavaScript gọi API                                 │
│     └─ Hiển thị kết quả                                   │
│                                                            │
└────────────────────────────────────────────────────────────┘

LUỒNG DỮ LIỆU:
User → Browser → GET http://localhost:8080/multi_demo.html
                     ↓
            Tải HTML/CSS/JS về
                     ↓
User nhập data → Click "Dự đoán"
                     ↓
Browser → POST http://localhost:8080/predict/wine (hoặc /customer)
                     ↓
Flask API → Load model → Dự đoán → Trả JSON
                     ↓
Browser ← Nhận JSON ← Hiển thị kết quả
```

---

## 💻 CHẠY TRÊN MÁY TÍNH

### 1. Cài đặt dependencies
```bash
cd D:\ML_04\ML_04\API
pip install -r requirements_api.txt
```

### 2. Khởi động server
```bash
python multi_api.py
```
✅ Thấy: `Server running on: http://localhost:8080`

### 3. Mở trình duyệt
```
http://localhost:8080
```

### 4. Test API
- Chọn tab **Wine Quality** hoặc **Customer Segmentation**
- Nhập dữ liệu
- Click "Dự đoán"

---

## 📱 CHẠY TRÊN ĐIỆN THOẠI

### Bước 1: Lấy IP máy tính
```bash
ipconfig
# Tìm dòng: IPv4 Address. . . : 192.168.1.100
#                                ^^^^^^^^^^^^^^
```

### Bước 2: Đảm bảo cùng WiFi
- ✅ Máy tính: WiFi "TenWiFi"
- ✅ Điện thoại: WiFi "TenWiFi"
- ❌ KHÔNG: Máy tính WiFi, điện thoại 4G

### Bước 3: Tắt Firewall Windows
```
Windows + R → firewall.cpl
→ Turn Windows Defender Firewall on or off
→ Chọn "Turn off" (Private + Public)
→ OK
```

### Bước 4: Mở trên điện thoại
```
http://192.168.1.100:8080
      ^^^^^^^^^^^^^^
      (IP máy tính của bạn)
```

### Bước 6: Test kết nối
```
http://192.168.1.100:8080/health

✅ Phải thấy:
{
  "status": "healthy",
  "models": {...}
}
```

---

## 🔍 XỬ LÝ LỖI

### Lỗi: Port đã được sử dụng
```bash
# Tìm process
netstat -ano | findstr :8080

# Kill process
taskkill /PID <số_PID> /F
```

### Lỗi: Không kết nối từ điện thoại
- ✅ Kiểm tra cùng WiFi
- ✅ Tắt Firewall
- ✅ Ping từ điện thoại: `ping 192.168.1.100`
- ✅ Test API: `http://<IP>:8080/health`

### Lỗi: Failed to fetch
- ✅ Server đang chạy?
- ✅ URL đúng không?
- ✅ CORS enabled trong `multi_api.py`?

---

## 📡 API ENDPOINTS

### **GET /** - Trang chủ web
```
http://localhost:8080/api
```

### **GET /health** - Kiểm tra trạng thái
```bash
curl http://localhost:8080/health
```

### **POST /predict/wine** - Dự đoán Wine Quality
```json
{
  "fixed_acidity": 7.4,
  "volatile_acidity": 0.7,
  "citric_acid": 0.0,
  "chlorides": 0.076,
  "total_sulfur_dioxide": 34.0,
  "density": 0.9978,
  "sulphates": 0.56,
  "alcohol": 9.4
}
```

### **POST /predict/customer** - Dự đoán Customer Segment
```json
{
  "annual_income": 50000,
  "spending_score": 50
}
```

### **GET /model_info** - Thông tin models
```bash
curl http://localhost:8080/model_info
```

---

## 🎯 TÓM TẮT NHANH

### Máy tính:
```bash
cd D:\ML_04\ML_04\API
python multi_api.py
# Mở: http://localhost:8080
```

### Điện thoại:
```bash
1. ipconfig → Lấy IP (VD: 192.168.1.100)
2. Cùng WiFi + Tắt Firewall
3. python multi_api.py
4. Mở: http://192.168.1.100:8080
```

---

## 📊 DANH SÁCH 8 FEATURES (Wine Quality)

1. `fixed_acidity` - Axit cố định
2. `volatile_acidity` - Axit bay hơi
3. `citric_acid` - Axit citric
4. `chlorides` - Ion Clorua
5. `total_sulfur_dioxide` - Tổng SO₂
6. `density` - Khối lượng riêng
7. `sulphates` - Ion sunfat
8. `alcohol` - Nồng độ ethanol

---

## ⚙️ CẤU HÌNH

### Thay đổi port:
```python
# multi_api.py, dòng cuối:
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Tắt debug mode:
```python
app.run(debug=False, host='0.0.0.0', port=8080)
```

---

## 📝 CHECKLIST

### Localhost:
- [ ] Có 3 file models trong `models/`
- [ ] `pip install -r requirements_api.txt`
- [ ] `python multi_api.py`
- [ ] Mở `http://localhost:8080`
- [ ] Test dự đoán thành công

### Mobile:
- [ ] `ipconfig` → ghi IP
- [ ] Cùng WiFi
- [ ] Tắt Firewall
- [ ] `python multi_api.py`
- [ ] Test: `http://<IP>:8080/health`
- [ ] Mở: `http://<IP>:8080`
- [ ] Test dự đoán thành công
