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
