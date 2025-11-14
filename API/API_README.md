# 🍷 Wine Quality Prediction API

API Flask để dự đoán chất lượng rượu vang đỏ dựa trên mô hình RandomForest đã huấn luyện.

## 📋 Yêu cầu

```bash
pip install -r requirements_api.txt
```

Hoặc cài đặt thủ công:
```bash
pip install Flask flask-cors joblib numpy pandas scikit-learn
```

## 🚀 Cách chạy API

### 1. Đảm bảo có file model
File `rf_winequality_best.joblib` phải nằm cùng thư mục với `api.py`

### 2. Chạy server
```bash
python api.py
```

Server sẽ chạy tại: `http://localhost:5000`

### 3. Truy cập từ thiết bị khác
- Lấy địa chỉ IP của máy: `ipconfig` (Windows) hoặc `ifconfig` (Linux/Mac)
- Truy cập từ mobile/web: `http://<your-ip>:5000`

## 📡 API Endpoints

### 1. **GET /** - Trang chủ
Hiển thị hướng dẫn sử dụng API

```bash
curl http://localhost:5000/
```

### 2. **GET /health** - Kiểm tra trạng thái
Kiểm tra API và model có hoạt động không

```bash
curl http://localhost:5000/health
```

### 3. **POST /predict** - Dự đoán 1 mẫu
Dự đoán chất lượng rượu cho 1 mẫu

**Request:**
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

**Response:**
```json
{
    "quality": "Bad (<6)",
    "prediction": 0,
    "probability": {
        "Bad (<6)": 0.65,
        "Good (≥6)": 0.35
    },
    "confidence": 0.65,
    "input_features": { ... }
}
```

**Ví dụ với curl:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "fixed_acidity": 7.4,
    "volatile_acidity": 0.7,
    "citric_acid": 0.0,
    "chlorides": 0.076,
    "total_sulfur_dioxide": 34.0,
    "density": 0.9978,
    "sulphates": 0.56,
    "alcohol": 9.4
  }'
```

**Ví dụ với Python:**
```python
import requests

url = "http://localhost:5000/predict"
data = {
    "fixed_acidity": 7.4,
    "volatile_acidity": 0.7,
    "citric_acid": 0.0,
    "chlorides": 0.076,
    "total_sulfur_dioxide": 34.0,
    "density": 0.9978,
    "sulphates": 0.56,
    "alcohol": 9.4
}

response = requests.post(url, json=data)
result = response.json()
print(result)
```

**Ví dụ với JavaScript (Fetch API):**
```javascript
fetch('http://localhost:5000/predict', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        fixed_acidity: 7.4,
        volatile_acidity: 0.7,
        citric_acid: 0.0,
        chlorides: 0.076,
        total_sulfur_dioxide: 34.0,
        density: 0.9978,
        sulphates: 0.56,
        alcohol: 9.4
    })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

### 4. **POST /batch_predict** - Dự đoán nhiều mẫu
Dự đoán chất lượng rượu cho nhiều mẫu cùng lúc

**Request:**
```json
{
    "samples": [
        {
            "fixed_acidity": 7.4,
            "volatile_acidity": 0.7,
            "citric_acid": 0.0,
            "chlorides": 0.076,
            "total_sulfur_dioxide": 34.0,
            "density": 0.9978,
            "sulphates": 0.56,
            "alcohol": 9.4
        },
        {
            "fixed_acidity": 8.1,
            "volatile_acidity": 0.6,
            "citric_acid": 0.3,
            "chlorides": 0.08,
            "total_sulfur_dioxide": 45.0,
            "density": 0.998,
            "sulphates": 0.65,
            "alcohol": 10.5
        }
    ]
}
```

**Response:**
```json
{
    "predictions": [
        {
            "sample_index": 0,
            "quality": "Bad (<6)",
            "prediction": 0,
            "probability": {
                "Bad (<6)": 0.65,
                "Good (≥6)": 0.35
            },
            "confidence": 0.65
        },
        {
            "sample_index": 1,
            "quality": "Good (≥6)",
            "prediction": 1,
            "probability": {
                "Bad (<6)": 0.25,
                "Good (≥6)": 0.75
            },
            "confidence": 0.75
        }
    ],
    "total_samples": 2
}
```

### 5. **GET /model_info** - Thông tin model
Lấy thông tin chi tiết về model đang sử dụng

```bash
curl http://localhost:5000/model_info
```

## 🌐 Web Demo

Mở file `web_demo.html` trong trình duyệt để sử dụng giao diện web đẹp mắt:

```bash
# Cách 1: Mở trực tiếp file HTML
start web_demo.html  # Windows
open web_demo.html   # Mac
xdg-open web_demo.html  # Linux

# Cách 2: Sử dụng Python HTTP server
python -m http.server 8080
# Sau đó truy cập: http://localhost:8080/web_demo.html
```

**Lưu ý:** Nhớ cập nhật địa chỉ API trong web demo nếu chạy trên máy khác!

## 📱 Tích hợp với Mobile (React Native)

```javascript
// Example with React Native
const predictWineQuality = async (wineData) => {
  try {
    const response = await fetch('http://192.168.1.100:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(wineData),
    });
    
    const result = await response.json();
    console.log('Prediction:', result);
    return result;
  } catch (error) {
    console.error('Error:', error);
  }
};

// Sử dụng
const wineData = {
  fixed_acidity: 7.4,
  volatile_acidity: 0.7,
  citric_acid: 0.0,
  chlorides: 0.076,
  total_sulfur_dioxide: 34.0,
  density: 0.9978,
  sulphates: 0.56,
  alcohol: 9.4
};

predictWineQuality(wineData);
```

## 📊 8 Features cần thiết

API yêu cầu 8 features sau (theo đúng thứ tự):

1. **fixed_acidity** - Axit cố định (g/L)
2. **volatile_acidity** - Axit bay hơi (g/L)
3. **citric_acid** - Axit citric (g/L)
4. **chlorides** - Ion Clorua (g/L)
5. **total_sulfur_dioxide** - Tổng SO₂ (mg/L)
6. **density** - Khối lượng riêng (g/cm³)
7. **sulphates** - Ion sunfat (g/L)
8. **alcohol** - Nồng độ ethanol (%)

## ⚠️ Xử lý lỗi

### Lỗi thiếu features:
```json
{
    "error": "Thiếu features",
    "missing_features": ["alcohol", "density"],
    "required_features": [...]
}
```

### Lỗi model chưa load:
```json
{
    "error": "Model chưa được load"
}
```

### Lỗi dự đoán:
```json
{
    "error": "Lỗi khi dự đoán: <chi tiết lỗi>"
}
```

## 🔧 Cấu hình nâng cao

### Thay đổi port:
```python
# Trong api.py, dòng cuối:
app.run(debug=True, host='0.0.0.0', port=8080)  # Đổi port thành 8080
```

### Tắt debug mode (production):
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

### Giới hạn CORS:
```python
# Trong api.py, thay:
CORS(app)
# Thành:
CORS(app, resources={r"/*": {"origins": "http://yourdomain.com"}})
```

## 🐛 Troubleshooting

### API không chạy được:
```bash
# Kiểm tra port đã được sử dụng chưa:
netstat -ano | findstr :5000  # Windows
lsof -i :5000  # Mac/Linux

# Kill process đang dùng port:
taskkill /PID <PID> /F  # Windows
kill -9 <PID>  # Mac/Linux
```

### Không kết nối được từ thiết bị khác:
- Tắt Firewall hoặc cho phép port 5000
- Đảm bảo cùng mạng WiFi
- Kiểm tra IP: `ipconfig` (Windows) hoặc `ifconfig` (Mac/Linux)

### Model không load được:
```bash
# Kiểm tra file model:
ls -lh rf_winequality_best.joblib

# Tạo lại model nếu cần:
# Chạy notebook Do_An_1.ipynb từ đầu
```

## 📝 License

Educational project - Free to use

## 👨‍💻 Author

ML_04 - Wine Quality Classification Project


# 🔌 TẠI SAO PORT 5000 VÀ 8080 VẪN HIỂU NHAU?

## ❓ CÂU HỎI: Khác port sao vẫn giao tiếp được?

**Câu trả lời ngắn gọn:**
> Chúng **KHÔNG** trực tiếp "hiểu nhau"! 
> Frontend (port 8080) **CHỦ ĐỘNG GỌI** Backend (port 5000) thông qua URL đầy đủ.

---

## 🎯 GIẢI THÍCH CHI TIẾT

### **1. HAI SERVER HOÀN TOÀN ĐỘC LẬP**

```
┌─────────────────────────────┐      ┌─────────────────────────────┐
│  SERVER 1: Static Files     │      │  SERVER 2: Flask API        │
│  Port: 8080                 │      │  Port: 5000                 │
│  http://localhost:8080      │      │  http://localhost:5000      │
│                             │      │                             │
│  Chỉ serve HTML/CSS/JS      │      │  Chỉ xử lý API requests     │
│  KHÔNG biết Flask tồn tại   │      │  KHÔNG biết HTML ở đâu      │
└─────────────────────────────┘      └─────────────────────────────┘
         │                                      ▲
         │                                      │
         └──────────────────────────────────────┘
              Browser làm cầu nối!
```

---

## 🌐 LUỒNG HOẠT ĐỘNG THỰC TẾ

### **BƯỚC 1: User mở trình duyệt**

```
User gõ: http://localhost:8080/multi_demo.html
```

**Điều gì xảy ra?**

```
Browser ──────GET Request──────► Static File Server (Port 8080)
                                  │
                                  │ Tìm file multi_demo.html
                                  │
Browser ◄─────File HTML────────── │
```

**Kết quả:** Browser nhận được file HTML + CSS + JavaScript

---

### **BƯỚC 2: Browser render HTML**

```html
<!-- File multi_demo.html được tải về máy user -->
<!DOCTYPE html>
<html>
<head>...</head>
<body>
    <form id="wineForm">...</form>
    
    <script>
        // JavaScript này CHẠY TRÊN BROWSER, không phải server!
        const API_URL = 'http://localhost:5000';  // ← URL Flask API
        
        document.getElementById('wineForm').addEventListener('submit', async (e) => {
            // Code này sẽ chạy khi user click nút
        });
    </script>
</body>
</html>
```

**Quan trọng:** 
- HTML/JavaScript đã được **tải về browser**
- Không còn liên quan gì đến port 8080 nữa!
- JavaScript chạy **trên máy user**, không phải server

---

### **BƯỚC 3: User submit form**

**Đây là lúc magic xảy ra!**

```javascript
// Code này chạy TRONG BROWSER của user
const response = await fetch('http://localhost:5000/predict/wine', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
});
```

**Phân tích:**

```
┌──────────────────────────────────────────────────────────────────┐
│ BROWSER (trên máy user)                                          │
│                                                                  │
│ 1. JavaScript đọc URL: 'http://localhost:5000/predict/wine'    │
│                                                                  │
│ 2. Browser tạo HTTP Request MỚI:                                │
│    - Đích đến: localhost:5000 (KHÔNG PHẢI 8080!)               │
│    - Method: POST                                               │
│    - Body: JSON data                                            │
│                                                                  │
│ 3. Browser GỬI request tới port 5000                           │
└──────────────────────────────────────────────────────────────────┘
         │
         │ HTTP POST Request
         │
         ▼
┌──────────────────────────────────────────────────────────────────┐
│ FLASK API (Port 5000)                                           │
│                                                                  │
│ 1. Nhận request từ browser                                      │
│ 2. Xử lý với Python code                                        │
│ 3. Trả về JSON response                                         │
└──────────────────────────────────────────────────────────────────┘
         │
         │ HTTP Response
         │
         ▼
┌──────────────────────────────────────────────────────────────────┐
│ BROWSER (JavaScript nhận response)                              │
│                                                                  │
│ const result = await response.json();                           │
│ displayResult(result);  // Hiển thị lên HTML                    │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔑 ĐIỂM QUAN TRỌNG

### **Port 8080 chỉ dùng 1 LẦN DUY NHẤT!**

```
User → Browser → http://localhost:8080/multi_demo.html
                        ↓
                  Tải file HTML về
                        ↓
            HTML/JS đã ở trên browser
                        ↓
        KHÔNG DÙNG PORT 8080 NỮA!
```

### **Mọi request sau đó đều tới Port 5000**

```javascript
// Trong code JavaScript (đã tải về browser)

// Request 1: Dự đoán Wine
fetch('http://localhost:5000/predict/wine', {...})

// Request 2: Dự đoán Customer  
fetch('http://localhost:5000/predict/customer', {...})

// Request 3: Health check
fetch('http://localhost:5000/health', {...})

// TẤT CẢ đều gọi tới port 5000, KHÔNG PHẢI 8080!
```

---

## 📱 VÍ DỤ THỰC TẾ DỄ HIỂU

### **Ví dụ 1: Như đọc sách**

```
1. Bạn mua sách từ hiệu sách (Port 8080)
   → Nhận sách về nhà
   
2. Đọc sách, thấy số điện thoại hotline trong sách
   → Gọi điện thoại tới hotline (Port 5000)
   
3. Hotline trả lời câu hỏi
   → Bạn nhận thông tin

📌 Hiệu sách (8080) KHÔNG liên quan gì đến cuộc gọi!
   Bạn gọi TRỰC TIẾP tới hotline (5000)
```

### **Ví dụ 2: Như gọi Grab**

```
1. Tải app Grab từ App Store (Port 8080)
   → App được cài vào điện thoại
   
2. Mở app, click "Đặt xe"
   → App gọi API tới server Grab (Port 5000)
   
3. Server Grab xử lý và trả về thông tin xe
   → App hiển thị

📌 App Store KHÔNG tham gia vào việc đặt xe!
   App gọi TRỰC TIẾP tới Grab server
```

---

## 🔍 KIỂM CHỨNG BẰNG BROWSER DEVTOOLS

### **Cách xem trong Chrome:**

1. Mở `http://localhost:8080/multi_demo.html`
2. Nhấn **F12** → Tab **Network**
3. Submit form dự đoán
4. Xem các request:

```
┌────────────────────────────────────────────────────────────────┐
│ Network Tab - Tất cả HTTP Requests                             │
├────────────────────────────────────────────────────────────────┤
│ Name              | Status | Type | Size | Time | Domain       │
├────────────────────────────────────────────────────────────────┤
│ multi_demo.html   | 200    | html | 50KB | 10ms | :8080 ✓     │
│                   |        |      |      |      | (Chỉ 1 lần) │
├────────────────────────────────────────────────────────────────┤
│ predict/wine      | 200    | xhr  | 2KB  | 50ms | :5000 ✓     │
│ predict/customer  | 200    | xhr  | 1KB  | 30ms | :5000 ✓     │
│ health            | 200    | xhr  | 500B | 10ms | :5000 ✓     │
│ predict/wine      | 200    | xhr  | 2KB  | 45ms | :5000 ✓     │
└────────────────────────────────────────────────────────────────┘

📊 Phân tích:
   - Port 8080: Chỉ 1 request (tải HTML)
   - Port 5000: Nhiều requests (API calls)
```

---

## 🎨 SƠ ĐỒ ĐẦY ĐỦ VỚI TIMELINE

```
TIME   │ ACTOR          │ ACTION                        │ PORT
───────┼────────────────┼───────────────────────────────┼─────────
00:00  │ User           │ Gõ URL vào browser            │ -
       │                │ http://localhost:8080/...     │
       │                │                               │
00:01  │ Browser        │ GET request                   │ → 8080
       │                │                               │
00:02  │ Static Server  │ Trả về file HTML              │ 8080 →
       │ (Port 8080)    │                               │
       │                │                               │
00:03  │ Browser        │ Render HTML                   │ -
       │                │ Load JavaScript               │
       │                │                               │
       │ [Port 8080 KHÔNG DÙNG NỮA TỪ ĐÂY]            │
       │                │                               │
00:10  │ User           │ Nhập data, click "Dự đoán"   │ -
       │                │                               │
00:11  │ JavaScript     │ fetch() tạo request           │ -
       │ (in Browser)   │ URL: localhost:5000/predict.. │
       │                │                               │
00:12  │ Browser        │ POST request                  │ → 5000
       │                │                               │
00:13  │ Flask API      │ Nhận request                  │ 5000
       │ (Port 5000)    │ Xử lý với ML model            │
       │                │                               │
00:14  │ Flask API      │ Trả về JSON response          │ 5000 →
       │                │                               │
00:15  │ Browser        │ Nhận response                 │ -
       │ (JavaScript)   │ Update HTML                   │
       │                │                               │
00:20  │ User           │ Click "Dự đoán" lần 2         │ -
       │                │                               │
00:21  │ JavaScript     │ fetch() request mới           │ → 5000
       │                │                               │
       │ [Lặp lại, vẫn chỉ dùng port 5000]            │
```

---

## 💡 VẬY TẠI SAO CORS QUAN TRỌNG?

### **Không có CORS:**

```python
# Flask API (multi_api.py)
app = Flask(__name__)
# KHÔNG CÓ: CORS(app)

@app.route('/predict/wine', methods=['POST'])
def predict_wine():
    return jsonify({...})
```

**Kết quả:**
```
Browser Console:
❌ Access to fetch at 'http://localhost:5000/predict/wine' 
   from origin 'http://localhost:8080' has been blocked by CORS policy
```

**Tại sao?**
- Browser security: Chặn requests từ domain khác
- HTML tải từ `localhost:8080`
- JavaScript gọi tới `localhost:5000` (khác domain!)
- Browser nói: "Ơ ơ, suspicious! Chặn lại!"

### **Có CORS:**

```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # ← Nói với Browser: "It's okay, tôi cho phép!"
```

**Kết quả:**
```
✅ Request thành công!
```

**CORS là gì?**
- **C**ross-**O**rigin **R**esource **S**haring
- Header đặc biệt nói: "Tôi cho phép requests từ origins khác"
- Flask API trả về header: `Access-Control-Allow-Origin: *`
- Browser đọc header → "OK, được phép!" → Cho phép request

---

## 🧪 THỰC NGHIỆM ĐỂ HIỂU RÕ

### **Test 1: Tắt Flask API (Port 5000)**

```bash
# Tắt Flask server
# Chỉ giữ lại HTTP server (Port 8080)
```

**Kết quả:**
```
✅ http://localhost:8080/multi_demo.html → Vẫn mở được!
   (HTML/CSS/JS vẫn hiển thị bình thường)

❌ Click "Dự đoán" → Lỗi!
   Error: Failed to fetch
   (Không kết nối được tới port 5000)
```

### **Test 2: Tắt Static Server (Port 8080)**

```bash
# Tắt HTTP server
# Chỉ giữ lại Flask (Port 5000)
```

**Kết quả:**
```
❌ http://localhost:8080/multi_demo.html → Không mở được!
   (Không có gì serve HTML file)

✅ http://localhost:5000/ → Vẫn hoạt động!
   (Flask API documentation vẫn chạy)
```

### **Test 3: Thay đổi API URL trong HTML**

```javascript
// Thay đổi trong multi_demo.html
const response = await fetch('http://localhost:9999/predict/wine', {
    // Đổi từ 5000 → 9999
});
```

**Kết quả:**
```
❌ Lỗi: Failed to fetch
   (Port 9999 không có gì chạy)
```

**Kết luận:** 
- Frontend phải **CHỈ ĐỊNH RÕ** địa chỉ Backend
- Không có magic, không tự động tìm!

---

## 📚 TÓM TẮT

### **Câu trả lời cho câu hỏi ban đầu:**

```
┌─────────────────────────────────────────────────────────────────┐
│ "Sao port 5000 vs 8080 mà vẫn hiểu nhau?"                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ TRẠNG THÁI: Chúng KHÔNG tự động "hiểu nhau"                    │
│                                                                 │
│ THỰC TẾ:                                                        │
│                                                                 │
│ 1. Port 8080: Chỉ dùng 1 lần để tải HTML về browser           │
│                                                                 │
│ 2. JavaScript (đã ở browser) GỌI TRỰC TIẾP tới port 5000      │
│    thông qua URL đầy đủ: http://localhost:5000/...            │
│                                                                 │
│ 3. Browser làm cầu nối giữa user và Flask API                  │
│                                                                 │
│ 4. Hai server HOÀN TOÀN ĐỘC LẬP, không biết nhau tồn tại      │
│                                                                 │
│ 5. CORS cho phép Browser gọi từ origin này sang origin khác    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### **Công thức đơn giản:**

```
Port 8080: Tải HTML/CSS/JS về → XONG NHIỆM VỤ
              ↓
JavaScript (trong browser): Gọi API tới Port 5000
              ↓
Port 5000: Xử lý requests → Trả về JSON
              ↓
JavaScript: Nhận JSON → Update HTML
```

**Không có giao tiếp trực tiếp giữa 8080 và 5000!**  
**Browser là người trung gian kết nối tất cả!** 🌐
