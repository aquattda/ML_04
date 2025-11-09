# 🔄 LUỒNG GIAO TIẾP GIỮA MULTI_API.PY VÀ MULTI_DEMO.HTML

## 📊 KIẾN TRÚC TỔNG QUAN

```
┌─────────────────┐         HTTP Request (JSON)        ┌─────────────────┐
│                 │  ──────────────────────────────►   │                 │
│ multi_demo.html │                                    │  multi_api.py   │
│   (Frontend)    │                                    │   (Backend)     │
│  JavaScript     │  ◄──────────────────────────────   │     Flask       │
│                 │         HTTP Response (JSON)       │                 │
└─────────────────┘                                    └─────────────────┘
    Port: 8080                                             Port: 5000
```

---

## 🔗 CÁCH CHÚNG GIAO TIẾP

### **1. ĐỊA CHỈ KẾT NỐI (API URL)**

**Trong multi_demo.html (dòng 392):**
```html
<input type="text" id="apiUrl" value="http://localhost:5000" placeholder="http://localhost:5000">
```

- **`http://localhost:5000`** = Địa chỉ Flask API đang chạy
- Frontend (HTML) gửi request tới địa chỉ này
- Backend (Flask) đang lắng nghe ở port 5000

---

## 📝 LUỒNG HOẠT ĐỘNG CHI TIẾT

### **BƯỚC 1: Khởi động các Server**

#### **Terminal 1: Chạy Flask API**
```bash
cd D:\ML_04\ML_04\API
python multi_api.py
```
**Kết quả:**
```
============================================================
Multi-Model Prediction API
============================================================
Server running on: http://localhost:5000
Mobile/Web can access: http://<your-ip>:5000
============================================================
```

#### **Terminal 2: Chạy Web Server cho HTML**
```bash
cd D:\ML_04\ML_04\web
python -m http.server 8080
```
**Kết quả:**
```
Serving HTTP on :: port 8080 (http://[::]:8080/) ...
```

---

### **BƯỚC 2: User mở trình duyệt**

```
http://localhost:8080/multi_demo.html
```

---

### **BƯỚC 3: User nhập dữ liệu và Submit Form**

#### **VÍ DỤ 1: DỰ ĐOÁN CHẤT LƯỢNG RƯỢU**

**📱 Frontend (multi_demo.html) - JavaScript Code:**

```javascript
// User click nút "Dự đoán" trong Wine Quality form
document.getElementById('wineForm').addEventListener('submit', async (e) => {
    e.preventDefault();  // Ngăn form reload page
    
    // BƯỚC 3.1: Thu thập dữ liệu từ form
    const data = {
        fixed_acidity: parseFloat(document.getElementById('fixed_acidity').value),
        volatile_acidity: parseFloat(document.getElementById('volatile_acidity').value),
        citric_acid: parseFloat(document.getElementById('citric_acid').value),
        chlorides: parseFloat(document.getElementById('chlorides').value),
        total_sulfur_dioxide: parseFloat(document.getElementById('total_sulfur_dioxide').value),
        density: parseFloat(document.getElementById('density').value),
        sulphates: parseFloat(document.getElementById('sulphates').value),
        alcohol: parseFloat(document.getElementById('alcohol').value)
    };
    
    // BƯỚC 3.2: Gửi HTTP POST Request tới Flask API
    try {
        const apiUrl = document.getElementById('apiUrl').value;  // http://localhost:5000
        
        const response = await fetch(`${apiUrl}/predict/wine`, {
            method: 'POST',                              // HTTP method
            headers: {'Content-Type': 'application/json'}, // Nói với server là JSON
            body: JSON.stringify(data)                   // Chuyển object thành JSON string
        });
        
        // BƯỚC 3.3: Nhận response từ Flask
        const result = await response.json();  // Parse JSON response
        
        if (!response.ok) {
            throw new Error(result.error || 'Lỗi khi gọi API');
        }
        
        // BƯỚC 3.4: Hiển thị kết quả lên giao diện
        displayWineResult(result);
        
    } catch (err) {
        showError('wineError', `❌ Lỗi: ${err.message}`);
    }
});
```

**🔍 Chi tiết HTTP Request gửi đi:**

```http
POST http://localhost:5000/predict/wine HTTP/1.1
Content-Type: application/json

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

---

**🖥️ Backend (multi_api.py) - Xử lý Request:**

```python
@app.route('/predict/wine', methods=['POST'])
def predict_wine():
    """
    ENDPOINT nhận request từ Frontend
    """
    if wine_model is None:
        return jsonify({"error": "Wine Quality model chưa được load"}), 500
    
    try:
        # BƯỚC 4.1: Nhận JSON data từ request
        data = request.get_json()
        # data = {
        #     "fixed_acidity": 7.4,
        #     "volatile_acidity": 0.7,
        #     ...
        # }
        
        # BƯỚC 4.2: Validate - Kiểm tra đủ features chưa
        missing_features = [f for f in WINE_FEATURES if f not in data]
        if missing_features:
            return jsonify({
                "error": "Thiếu features cho Wine Quality",
                "missing_features": missing_features,
                "required_features": WINE_FEATURES
            }), 400
        
        # BƯỚC 4.3: Chuẩn bị dữ liệu cho model
        input_data = pd.DataFrame([[data[f] for f in WINE_FEATURES]], 
                                   columns=WINE_FEATURES)
        
        # BƯỚC 4.4: Dự đoán bằng ML model
        prediction = wine_model.predict(input_data)[0]      # 0 hoặc 1
        probability = wine_model.predict_proba(input_data)[0]  # [0.3, 0.7]
        
        # BƯỚC 4.5: Format kết quả
        quality_label = "Good (≥6)" if prediction == 1 else "Bad (<6)"
        confidence = float(max(probability))
        
        # BƯỚC 4.6: Trả về JSON response
        return jsonify({
            "model": "wine_quality",
            "quality": quality_label,
            "prediction": int(prediction),
            "probability": {
                "Bad (<6)": float(probability[0]),
                "Good (≥6)": float(probability[1])
            },
            "confidence": confidence,
            "input_features": data
        })
    
    except Exception as e:
        return jsonify({"error": f"Lỗi khi dự đoán Wine Quality: {str(e)}"}), 500
```

**🔍 HTTP Response trả về:**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "model": "wine_quality",
    "quality": "Bad (<6)",
    "prediction": 0,
    "probability": {
        "Bad (<6)": 0.73,
        "Good (≥6)": 0.27
    },
    "confidence": 0.73,
    "input_features": {
        "fixed_acidity": 7.4,
        "volatile_acidity": 0.7,
        ...
    }
}
```

---

### **BƯỚC 4: Frontend hiển thị kết quả**

**📱 JavaScript hiển thị kết quả (multi_demo.html):**

```javascript
function displayWineResult(result) {
    // result = {
    //     "quality": "Bad (<6)",
    //     "prediction": 0,
    //     "probability": {"Bad (<6)": 0.73, "Good (≥6)": 0.27},
    //     "confidence": 0.73
    // }
    
    const isGood = result.prediction === 1;
    const resultBox = document.getElementById('wineResult');
    
    // Thay đổi màu sắc theo kết quả
    resultBox.className = 'result-box wine ' + (isGood ? 'good' : 'bad');
    
    // Hiển thị kết quả
    document.getElementById('wineResultTitle').textContent = 
        `🍷 Chất lượng rượu: ${result.quality}`;
    
    document.getElementById('wineResultText').innerHTML = `
        <p><strong>Prediction:</strong> ${result.prediction === 1 ? 'Good' : 'Bad'}</p>
        <p><strong>Confidence:</strong> ${(result.confidence * 100).toFixed(1)}%</p>
        <div class="probability-bars">
            <div class="prob-bar">
                <span>Bad (&lt;6):</span>
                <div class="prob-fill bad" style="width: ${result.probability['Bad (<6)'] * 100}%">
                    ${(result.probability['Bad (<6)'] * 100).toFixed(1)}%
                </div>
            </div>
            <div class="prob-bar">
                <span>Good (≥6):</span>
                <div class="prob-fill good" style="width: ${result.probability['Good (≥6)'] * 100}%">
                    ${(result.probability['Good (≥6)'] * 100).toFixed(1)}%
                </div>
            </div>
        </div>
    `;
    
    // Hiển thị result box
    showElement('wineResult');
}
```

---

## 🔄 VÍ DỤ 2: PHÂN KHÚC KHÁCH HÀNG

### **Frontend Request:**

```javascript
// User nhập annual_income = 50, spending_score = 60
const data = {
    annual_income: parseFloat(document.getElementById('annual_income').value),
    spending_score: parseFloat(document.getElementById('spending_score').value)
};

const response = await fetch(`${apiUrl}/predict/customer`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
});
```

**HTTP Request gửi đi:**
```http
POST http://localhost:5000/predict/customer HTTP/1.1
Content-Type: application/json

{
    "annual_income": 50,
    "spending_score": 60
}
```

### **Backend xử lý:**

```python
@app.route('/predict/customer', methods=['POST'])
def predict_customer():
    data = request.get_json()
    # {"annual_income": 50, "spending_score": 60}
    
    # Chuẩn bị data
    input_data = np.array([[data["annual_income"], data["spending_score"]]])
    
    # Scaling
    input_scaled = scaler_model.transform(input_data)
    
    # Predict
    cluster = kmeans_model.predict(input_scaled)[0]  # Cluster number: 0-4
    
    # Trả về response
    return jsonify({
        "model": "customer_segmentation",
        "cluster": int(cluster),
        "cluster_meaning": CLUSTER_MEANINGS.get(cluster),
        "confidence": float(confidence),
        ...
    })
```

**HTTP Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "model": "customer_segmentation",
    "cluster": 2,
    "cluster_meaning": "Chuẩn mực - Thu nhập trung bình, Chi tiêu trung bình",
    "confidence": 0.85,
    "centroid_coordinates": {
        "annual_income": 55.2,
        "spending_score": 49.5
    }
}
```

---

## 🔑 ĐIỂM QUAN TRỌNG

### **1. CORS (Cross-Origin Resource Sharing)**

**Tại sao cần CORS?**

```python
# Trong multi_api.py
from flask_cors import CORS
CORS(app)  # ← CỰC KỲ QUAN TRỌNG!
```

- **Không có CORS:** Browser sẽ chặn request từ `localhost:8080` → `localhost:5000`
- **Có CORS:** Cho phép HTML từ domain khác gọi API

**Lỗi nếu không có CORS:**
```
Access to fetch at 'http://localhost:5000/predict/wine' from origin 
'http://localhost:8080' has been blocked by CORS policy
```

---

### **2. JSON Format**

**Frontend gửi:**
```javascript
body: JSON.stringify(data)  // Chuyển object → JSON string
```

**Backend nhận:**
```python
data = request.get_json()  # Parse JSON string → Python dict
```

**Backend trả về:**
```python
return jsonify({...})  # Chuyển Python dict → JSON string
```

**Frontend nhận:**
```javascript
const result = await response.json()  // Parse JSON string → JavaScript object
```

---

### **3. Async/Await Pattern**

```javascript
// async cho phép dùng await
async (e) => {
    // await đợi response trước khi chạy tiếp
    const response = await fetch(`${apiUrl}/predict/wine`, {...});
    const result = await response.json();
    
    // Code này chỉ chạy sau khi có result
    displayWineResult(result);
}
```

---

## 🧪 CÁCH TEST LUỒNG GIAO TIẾP

### **Test 1: Kiểm tra API hoạt động**

**Browser hoặc Postman:**
```
GET http://localhost:5000/
```

**Expected Response:**
```json
{
    "message": "Multi-Model Prediction API",
    "version": "2.0",
    "models": {...},
    "endpoints": {...}
}
```

### **Test 2: Test với cURL (Command line)**

```bash
# Test Wine Prediction
curl -X POST http://localhost:5000/predict/wine ^
  -H "Content-Type: application/json" ^
  -d "{\"fixed_acidity\":7.4,\"volatile_acidity\":0.7,\"citric_acid\":0.0,\"chlorides\":0.076,\"total_sulfur_dioxide\":34.0,\"density\":0.9978,\"sulphates\":0.56,\"alcohol\":9.4}"

# Test Customer Segmentation
curl -X POST http://localhost:5000/predict/customer ^
  -H "Content-Type: application/json" ^
  -d "{\"annual_income\":50,\"spending_score\":60}"
```

### **Test 3: Browser Developer Tools**

1. Mở Chrome DevTools (F12)
2. Vào tab **Network**
3. Submit form trong multi_demo.html
4. Xem request/response chi tiết

---

## 📊 SƠ ĐỒ LUỒNG ĐẦY ĐỦ

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. USER MỞ BROWSER                                              │
│    http://localhost:8080/multi_demo.html                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. HTML FORM HIỂN THỊ                                           │
│    - Input fields cho Wine Quality (8 fields)                   │
│    - Input fields cho Customer (2 fields)                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. USER NHẬP DỮ LIỆU & CLICK "DỰ ĐOÁN"                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. JAVASCRIPT (Frontend)                                        │
│    - Thu thập data từ form                                      │
│    - Chuyển thành JSON                                          │
│    - Gửi HTTP POST request tới Flask API                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. FLASK API (Backend) nhận request                            │
│    - Parse JSON data                                            │
│    - Validate features                                          │
│    - Chuẩn bị input cho model                                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. MACHINE LEARNING MODEL                                       │
│    - Wine: RandomForest.predict()                               │
│    - Customer: KMeans.predict()                                 │
│    - Tính confidence scores                                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. FLASK API trả về JSON response                              │
│    - Kết quả dự đoán                                            │
│    - Probability scores                                         │
│    - Metadata                                                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 8. JAVASCRIPT (Frontend) nhận response                         │
│    - Parse JSON                                                 │
│    - Format data                                                │
│    - Update HTML elements                                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 9. KẾT QUẢ HIỂN THỊ TRÊN GIAO DIỆN                            │
│    - Prediction result                                          │
│    - Confidence bars                                            │
│    - Colored result box                                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✅ TÓM TẮT

**Hai file giao tiếp với nhau qua:**

1. **HTTP Protocol** - Request/Response
2. **JSON Format** - Trao đổi dữ liệu
3. **REST API** - Endpoints chuẩn
4. **Fetch API** - JavaScript gọi HTTP
5. **Flask Routes** - Python xử lý requests
6. **CORS** - Cho phép cross-origin

**Không có magic!** Chỉ là giao tiếp client-server chuẩn HTTP! 🚀
