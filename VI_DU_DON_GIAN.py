"""
ĐÂY LÀ VÍ DỤ ĐƠN GIẢN HÓA ĐỂ HIỂU LUỒNG GIAO TIẾP
========================================================

Giả sử bạn đang ở nhà hàng:
- multi_demo.html = Khách hàng (Frontend)
- multi_api.py = Bếp trưởng (Backend)
- HTTP Request = Phiếu order
- HTTP Response = Món ăn
"""

# ============================================================
# PHẦN 1: FLASK API (Backend - Bếp trưởng)
# File: multi_api.py
# ============================================================

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Cho phép khách hàng từ địa chỉ khác gọi vào

# Giả sử đây là model ML đã train (đơn giản hóa)
def predict_wine_quality(data):
    """Giả lập prediction - thực tế sẽ dùng ML model"""
    alcohol = data.get('alcohol', 0)
    if alcohol > 10:
        return {"quality": "Good", "confidence": 0.85}
    else:
        return {"quality": "Bad", "confidence": 0.73}

# ──────────────────────────────────────────────────────────
# ENDPOINT: Nhận order từ khách hàng
# ──────────────────────────────────────────────────────────
@app.route('/predict/wine', methods=['POST'])
def predict_wine():
    """
    BƯỚC 1 (Backend): Nhận request từ Frontend
    """
    print("📨 Backend nhận được request từ Frontend!")
    
    # BƯỚC 2: Lấy data từ request (phiếu order)
    data = request.get_json()
    print(f"📋 Data nhận được: {data}")
    
    # BƯỚC 3: Xử lý (nấu món)
    result = predict_wine_quality(data)
    print(f"✅ Kết quả: {result}")
    
    # BƯỚC 4: Trả về response (giao món)
    return jsonify({
        "model": "wine_quality",
        "quality": result["quality"],
        "confidence": result["confidence"],
        "input_received": data
    })

if __name__ == '__main__':
    print("🚀 Flask API đang chạy tại http://localhost:5000")
    app.run(port=5000)


# ============================================================
# PHẦN 2: HTML + JAVASCRIPT (Frontend - Khách hàng)
# File: demo_simple.html
# ============================================================

"""
<!DOCTYPE html>
<html>
<head>
    <title>Simple Demo</title>
</head>
<body>
    <h1>🍷 Wine Quality Prediction</h1>
    
    <!-- Form để user nhập liệu -->
    <form id="wineForm">
        <label>Alcohol Level:</label>
        <input type="number" id="alcohol" value="9.4" step="0.1">
        <button type="submit">Dự đoán</button>
    </form>
    
    <!-- Hiển thị kết quả -->
    <div id="result" style="display:none;">
        <h2>Kết quả:</h2>
        <p id="resultText"></p>
    </div>

    <script>
        // ──────────────────────────────────────────────────
        // JAVASCRIPT: Xử lý khi user submit form
        // ──────────────────────────────────────────────────
        
        document.getElementById('wineForm').addEventListener('submit', async (e) => {
            e.preventDefault();  // Ngăn reload page
            
            console.log('👤 User click nút Dự đoán!');
            
            // BƯỚC 1: Thu thập data từ form
            const alcoholValue = document.getElementById('alcohol').value;
            const data = {
                alcohol: parseFloat(alcoholValue),
                fixed_acidity: 7.4,
                volatile_acidity: 0.7,
                citric_acid: 0.0,
                chlorides: 0.076,
                total_sulfur_dioxide: 34.0,
                density: 0.9978,
                sulphates: 0.56
            };
            
            console.log('📦 Data chuẩn bị gửi:', data);
            
            // BƯỚC 2: Gửi HTTP Request tới Flask API
            try {
                console.log('📤 Đang gửi request tới http://localhost:5000/predict/wine');
                
                const response = await fetch('http://localhost:5000/predict/wine', {
                    method: 'POST',                            // Phương thức POST
                    headers: {
                        'Content-Type': 'application/json'     // Nói server là JSON
                    },
                    body: JSON.stringify(data)                 // Chuyển object → JSON string
                });
                
                console.log('✅ Nhận được response từ server!');
                
                // BƯỚC 3: Parse response JSON
                const result = await response.json();
                console.log('📨 Kết quả từ server:', result);
                
                // BƯỚC 4: Hiển thị kết quả lên giao diện
                document.getElementById('result').style.display = 'block';
                document.getElementById('resultText').innerHTML = `
                    <strong>Quality:</strong> ${result.quality}<br>
                    <strong>Confidence:</strong> ${(result.confidence * 100).toFixed(1)}%<br>
                    <strong>Model:</strong> ${result.model}
                `;
                
                console.log('🎉 Hiển thị kết quả thành công!');
                
            } catch (error) {
                console.error('❌ Lỗi:', error);
                alert('Lỗi khi gọi API: ' + error.message);
            }
        });
    </script>
</body>
</html>
"""


# ============================================================
# PHẦN 3: CONSOLE LOG KHI CHẠY (Minh họa)
# ============================================================

"""
┌──────────────────────────────────────────────────────────────┐
│ TERMINAL 1: Flask Server                                     │
├──────────────────────────────────────────────────────────────┤
│ $ python multi_api.py                                        │
│ 🚀 Flask API đang chạy tại http://localhost:5000            │
│                                                              │
│ [Đợi request...]                                             │
│                                                              │
│ 📨 Backend nhận được request từ Frontend!                    │
│ 📋 Data nhận được: {                                         │
│     'alcohol': 9.4,                                          │
│     'fixed_acidity': 7.4,                                    │
│     ...                                                      │
│ }                                                            │
│ ✅ Kết quả: {'quality': 'Bad', 'confidence': 0.73}          │
│ 127.0.0.1 - - [09/Nov/2025] "POST /predict/wine HTTP/1.1"   │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ BROWSER CONSOLE (F12 → Console tab)                         │
├──────────────────────────────────────────────────────────────┤
│ 👤 User click nút Dự đoán!                                   │
│ 📦 Data chuẩn bị gửi: {alcohol: 9.4, fixed_acidity: 7.4...} │
│ 📤 Đang gửi request tới http://localhost:5000/predict/wine  │
│ ✅ Nhận được response từ server!                             │
│ 📨 Kết quả từ server: {                                      │
│     model: "wine_quality",                                   │
│     quality: "Bad",                                          │
│     confidence: 0.73,                                        │
│     ...                                                      │
│ }                                                            │
│ 🎉 Hiển thị kết quả thành công!                              │
└──────────────────────────────────────────────────────────────┘
"""


# ============================================================
# PHẦN 4: HTTP REQUEST/RESPONSE THỰC TẾ
# ============================================================

"""
───────────────────────────────────────────────────────────────
REQUEST GỬI TỪ FRONTEND → BACKEND
───────────────────────────────────────────────────────────────

POST /predict/wine HTTP/1.1
Host: localhost:5000
Content-Type: application/json
Content-Length: 234

{
    "alcohol": 9.4,
    "fixed_acidity": 7.4,
    "volatile_acidity": 0.7,
    "citric_acid": 0.0,
    "chlorides": 0.076,
    "total_sulfur_dioxide": 34.0,
    "density": 0.9978,
    "sulphates": 0.56
}

───────────────────────────────────────────────────────────────
RESPONSE TỪ BACKEND → FRONTEND
───────────────────────────────────────────────────────────────

HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 156

{
    "model": "wine_quality",
    "quality": "Bad",
    "confidence": 0.73,
    "input_received": {
        "alcohol": 9.4,
        "fixed_acidity": 7.4,
        ...
    }
}
"""


# ============================================================
# PHẦN 5: CÁCH TEST BẰTAY
# ============================================================

"""
CÁCH 1: Dùng cURL (Command line)
─────────────────────────────────────────────────────────────

# Windows CMD/PowerShell
curl -X POST http://localhost:5000/predict/wine ^
  -H "Content-Type: application/json" ^
  -d "{\"alcohol\":9.4,\"fixed_acidity\":7.4,\"volatile_acidity\":0.7,\"citric_acid\":0.0,\"chlorides\":0.076,\"total_sulfur_dioxide\":34.0,\"density\":0.9978,\"sulphates\":0.56}"


CÁCH 2: Dùng Postman
─────────────────────────────────────────────────────────────

1. Method: POST
2. URL: http://localhost:5000/predict/wine
3. Headers:
   - Content-Type: application/json
4. Body (raw JSON):
{
    "alcohol": 9.4,
    "fixed_acidity": 7.4,
    "volatile_acidity": 0.7,
    "citric_acid": 0.0,
    "chlorides": 0.076,
    "total_sulfur_dioxide": 34.0,
    "density": 0.9978,
    "sulphates": 0.56
}


CÁCH 3: Browser DevTools
─────────────────────────────────────────────────────────────

1. Mở http://localhost:8080/multi_demo.html
2. Press F12 → Network tab
3. Submit form
4. Click vào request "predict/wine"
5. Xem Headers, Payload, Response
"""


# ============================================================
# PHẦN 6: TROUBLESHOOTING
# ============================================================

"""
LỖI THƯỜNG GẶP:
═══════════════════════════════════════════════════════════════

1. "Failed to fetch" / "NetworkError"
   → Flask API chưa chạy
   → Check: http://localhost:5000 có mở được không?

2. "CORS policy blocked"
   → Thiếu CORS(app) trong Flask
   → Thêm: from flask_cors import CORS; CORS(app)

3. "404 Not Found"
   → URL sai hoặc endpoint không tồn tại
   → Check: @app.route('/predict/wine') có đúng không?

4. "500 Internal Server Error"
   → Lỗi trong Python code (Backend)
   → Xem Terminal Flask để đọc error message

5. "JSON parse error"
   → Response không phải JSON hợp lệ
   → Check response.text trong Browser DevTools
"""


# ============================================================
# PHẦN 7: TẠI SAO CẦN 2 SERVER?
# ============================================================

"""
┌─────────────────────────────────────────────────────────────┐
│ Tại sao cần chạy 2 server riêng biệt?                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ SERVER 1: Flask API (Port 5000)                            │
│ ├─ Chỉ xử lý logic và ML models                            │
│ ├─ Trả về JSON (không phải HTML)                           │
│ └─ Backend pure API                                         │
│                                                             │
│ SERVER 2: HTTP Server (Port 8080)                          │
│ ├─ Serve static files (HTML, CSS, JS)                      │
│ ├─ Chỉ gửi file cho browser                                │
│ └─ Frontend pure                                            │
│                                                             │
│ LỢI ÍCH:                                                    │
│ ✓ Tách biệt Frontend/Backend (Clean Architecture)          │
│ ✓ API có thể dùng cho nhiều clients (Web, Mobile, Desktop) │
│ ✓ Deploy độc lập (Frontend lên CDN, Backend lên server)   │
│ ✓ Scale riêng biệt khi cần                                 │
└─────────────────────────────────────────────────────────────┘
"""

print(__doc__)
