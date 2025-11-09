"""
API Flask tổng hợp - Multi-Model Prediction
1. Dự đoán chất lượng rượu vang (Wine Quality)
2. Phân loại khách hàng K-Means (Customer Segmentation)

BƯỚC KHỞI TẠO API:
1. Import các thư viện cần thiết
2. Khởi tạo Flask app và cấu hình CORS
3. Định nghĩa đường dẫn tới các models
4. Load models từ file .joblib
5. Định nghĩa features cho từng model
6. Tạo các endpoints API
"""

# BƯỚC 1: IMPORT THƯ VIỆN 
from flask import Flask, request, jsonify  # Flask framework cho API
from flask_cors import CORS                # Cho phép cross-origin requests
import joblib                             # Để load models đã lưu
import numpy as np                        # Xử lý arrays
import pandas as pd                       # Xử lý data
import os                                 # Xử lý file paths

# BƯỚC 2: KHỞI TẠO FLASK APP 
app = Flask(__name__)                     # Tạo instance Flask
CORS(app)                                # Cho phép CORS để web/mobile có thể gọi API

# BƯỚC 3: ĐỊNH NGHĨA ĐƯỜNG DẪN MODEL
# Đường dẫn tương đối từ thư mục API/ tới thư mục models/
WINE_MODEL_PATH = "../models/rf_winequality_best.joblib"     # Random Forest model
KMEANS_MODEL_PATH = "../models/modelskmeans_mall.joblib"     # K-Means model
SCALER_MODEL_PATH = "../models/scaler_mall.joblib"          # StandardScaler

# BƯỚC 4: LOAD MODELS KHI KHỞI ĐỘNG SERVER
# Load Wine Quality Model (Random Forest)
try:
    wine_model = joblib.load(WINE_MODEL_PATH)
    print(f"Đã load Wine Quality model từ {WINE_MODEL_PATH}")
except Exception as e:
    print(f"Lỗi khi load Wine model: {e}")
    wine_model = None

# Load K-Means Model và Scaler
try:
    kmeans_model = joblib.load(KMEANS_MODEL_PATH)
    scaler_model = joblib.load(SCALER_MODEL_PATH)
    print(f"Đã load K-Means model từ {KMEANS_MODEL_PATH}")
    print(f"Đã load Scaler từ {SCALER_MODEL_PATH}")
except Exception as e:
    print(f"Lỗi khi load K-Means model: {e}")
    kmeans_model = None
    scaler_model = None

#   BƯỚC 5: ĐỊNH NGHĨA FEATURES CHO TỪNG MODEL  

# Features cho Wine Quality Model (8 features - Random Forest)
# Model này dự đoán chất lượng rượu vang từ 8 đặc tính hóa học
WINE_FEATURES = [
    "fixed_acidity",          # Độ axit cố định
    "volatile_acidity",       # Độ axit bay hơi
    "citric_acid",           # Axit citric
    "chlorides",             # Clorua
    "total_sulfur_dioxide",  # Tổng lưu huỳnh dioxide
    "density",               # Khối lượng riêng
    "sulphates",             # Sunfat
    "alcohol"                # Độ cồn
]

# Features cho Customer Segmentation Model (2 features - K-Means)
# Model này phân khúc khách hàng dựa trên thu nhập và điểm chi tiêu
CUSTOMER_FEATURES = [
    "annual_income",  # Thu nhập hàng năm (k$)
    "spending_score"  # Điểm chi tiêu (1-100)
]

#   BƯỚC 6: ĐỊNH NGHĨA BUSINESS LOGIC  

# Mapping cluster labels thành ý nghĩa business cho khách hàng
CLUSTER_MEANINGS = {
    0: "Tiết kiệm - Thu nhập thấp, Chi tiêu ít",
    1: "Cẩn thận - Thu nhập cao, Chi tiêu ít", 
    2: "Chuẩn mực - Thu nhập trung bình, Chi tiêu trung bình",
    3: "Mục tiêu - Thu nhập thấp, Chi tiêu cao",
    4: "VIP - Thu nhập cao, Chi tiêu cao"
}

#   BƯỚC 7: TẠO CÁC API ENDPOINTS  

@app.route('/')
def home():
    """
    ENDPOINT 1: Trang chủ API - Hướng dẫn sử dụng
    Method: GET
    Purpose: Cung cấp thông tin về API và các endpoints
    """
    return jsonify({
        "message": "Multi-Model Prediction API",
        "version": "2.0",
        "models": {
            "wine_quality": "Dự đoán chất lượng rượu vang",
            "customer_segmentation": "Phân loại khách hàng K-Means"
        },
        "endpoints": {
            "/": "Trang chủ (hướng dẫn)",
            "/health": "Kiểm tra trạng thái API",
            "/predict/wine": "POST - Dự đoán chất lượng rượu vang",
            "/predict/customer": "POST - Phân loại khách hàng",
            "/predict/batch": "POST - Dự đoán nhiều mẫu cùng lúc"
        },
        "wine_features": WINE_FEATURES,
        "customer_features": CUSTOMER_FEATURES,
        "examples": {
            "wine": {
                "fixed_acidity": 7.4,
                "volatile_acidity": 0.7,
                "citric_acid": 0.0,
                "chlorides": 0.076,
                "total_sulfur_dioxide": 34.0,
                "density": 0.9978,
                "sulphates": 0.56,
                "alcohol": 9.4
            },
            "customer": {
                "annual_income": 50,
                "spending_score": 60
            }
        }
    })
    
    

@app.route('/health', methods=['GET'])
def health():
    """
    ENDPOINT 2: Health Check - Kiểm tra trạng thái API
    Method: GET
    Purpose: Kiểm tra xem API và các models đã load thành công hay chưa
    """
    return jsonify({
        "status": "ok",
        "models": {
            "wine_model": wine_model is not None,
            "kmeans_model": kmeans_model is not None,
            "scaler_model": scaler_model is not None
        }
    })

@app.route('/predict/wine', methods=['POST'])
def predict_wine():
    """
    ENDPOINT 3: Wine Quality Prediction - Dự đoán chất lượng rượu vang
    Method: POST
    Purpose: Dự đoán chất lượng rượu vang từ 8 đặc tính hóa học
    
    Input: JSON với 8 features
    Output: Predicted quality score (3-8)
    """
    if wine_model is None:
        return jsonify({"error": "Wine Quality model chưa được load"}), 500
    
    try:
        data = request.get_json()
        # Kiểm tra features
        missing_features = [f for f in WINE_FEATURES if f not in data]
        if missing_features:
            return jsonify({
                "error": "Thiếu features cho Wine Quality",
                "missing_features": missing_features,
                "required_features": WINE_FEATURES
            }), 400
        # Tạo DataFrame
        input_data = pd.DataFrame([[data[f] for f in WINE_FEATURES]], 
                                   columns=WINE_FEATURES)
        # Dự đoán
        prediction = wine_model.predict(input_data)[0]
        probability = wine_model.predict_proba(input_data)[0]
        # Format kết quả
        quality_label = "Good (≥6)" if prediction == 1 else "Bad (<6)"
        confidence = float(max(probability))
        
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

@app.route('/predict/customer', methods=['POST'])
def predict_customer():
    """
    ENDPOINT 4: Customer Segmentation - Phân loại khách hàng K-Means
    Method: POST
    Purpose: Phân khúc khách hàng dựa trên thu nhập và điểm chi tiêu
    
    Input: JSON với 2 features (annual_income, spending_score)
    Output: Cluster number (0-4) và business meaning
    
    Request body example (JSON):
    {
        "annual_income": 50,
        "spending_score": 60
    }
    """
    if kmeans_model is None or scaler_model is None:
        return jsonify({"error": "Customer Segmentation models chưa được load"}), 500
    
    try:
        data = request.get_json()
        
        # Kiểm tra features
        missing_features = [f for f in CUSTOMER_FEATURES if f not in data]
        if missing_features:
            return jsonify({
                "error": "Thiếu features cho Customer Segmentation",
                "missing_features": missing_features,
                "required_features": CUSTOMER_FEATURES
            }), 400
        # Chuẩn bị dữ liệu (theo thứ tự của training)
        # K-Means model được train với ['Annual Income (k$)', 'Spending Score (1-100)']
        input_data = np.array([[data["annual_income"], data["spending_score"]]])
        # Scaling (như trong training)
        input_scaled = scaler_model.transform(input_data)
        # Dự đoán cluster
        cluster = kmeans_model.predict(input_scaled)[0]
        # Lấy khoảng cách đến các centroids
        distances = kmeans_model.transform(input_scaled)[0]
        confidence = 1 - (distances[cluster] / np.sum(distances))  # Confidence score
        # Lấy centroids gốc (unscaled)
        centroids_scaled = kmeans_model.cluster_centers_
        centroids_orig = scaler_model.inverse_transform(centroids_scaled)
        return jsonify({
            "model": "customer_segmentation",
            "cluster": int(cluster),
            "cluster_meaning": CLUSTER_MEANINGS.get(cluster, f"Cluster {cluster}"),
            "confidence": float(confidence),
            "distances_to_centroids": distances.tolist(),
            "centroid_coordinates": {
                "annual_income": float(centroids_orig[cluster][0]),
                "spending_score": float(centroids_orig[cluster][1])
            },
            "all_centroids": [
                {
                    "cluster": i,
                    "meaning": CLUSTER_MEANINGS.get(i, f"Cluster {i}"),
                    "annual_income": float(centroids_orig[i][0]),
                    "spending_score": float(centroids_orig[i][1])
                }
                for i in range(len(centroids_orig))
            ],
            "input_features": data
        })
    except Exception as e:
        return jsonify({"error": f"Lỗi khi phân loại Customer: {str(e)}"}), 500

@app.route('/predict/batch', methods=['POST'])
def predict_batch():
    """
    Dự đoán nhiều mẫu cùng lúc (cả wine và customer)
    
    Request body (JSON):
    {
        "wine_samples": [
            {
                "fixed_acidity": 7.4,
                "volatile_acidity": 0.7,
                ...
            }
        ],
        "customer_samples": [
            {
                "annual_income": 50,
                "spending_score": 60
            }
        ]
    }
    """
    try:
        data = request.get_json()
        results = {
            "wine_predictions": [],
            "customer_predictions": []
        }
        
        # Xử lý Wine samples
        if "wine_samples" in data and wine_model is not None:
            for idx, sample in enumerate(data["wine_samples"]):
                try:
                    # Kiểm tra features
                    missing = [f for f in WINE_FEATURES if f not in sample]
                    if missing:
                        results["wine_predictions"].append({
                            "sample_index": idx,
                            "error": f"Thiếu features: {missing}"
                        })
                        continue
                    
                    # Dự đoán
                    input_data = pd.DataFrame([[sample[f] for f in WINE_FEATURES]], 
                                            columns=WINE_FEATURES)
                    prediction = wine_model.predict(input_data)[0]
                    probability = wine_model.predict_proba(input_data)[0]
                    
                    quality_label = "Good (≥6)" if prediction == 1 else "Bad (<6)"
                    
                    results["wine_predictions"].append({
                        "sample_index": idx,
                        "quality": quality_label,
                        "prediction": int(prediction),
                        "probability": {
                            "Bad (<6)": float(probability[0]),
                            "Good (≥6)": float(probability[1])
                        },
                        "confidence": float(max(probability))
                    })
                except Exception as e:
                    results["wine_predictions"].append({
                        "sample_index": idx,
                        "error": str(e)
                    })
        
        # Xử lý Customer samples
        if "customer_samples" in data and kmeans_model is not None and scaler_model is not None:
            for idx, sample in enumerate(data["customer_samples"]):
                try:
                    # Kiểm tra features
                    missing = [f for f in CUSTOMER_FEATURES if f not in sample]
                    if missing:
                        results["customer_predictions"].append({
                            "sample_index": idx,
                            "error": f"Thiếu features: {missing}"
                        })
                        continue
                    # Dự đoán
                    input_data = np.array([[sample["annual_income"], sample["spending_score"]]])
                    input_scaled = scaler_model.transform(input_data)
                    cluster = kmeans_model.predict(input_scaled)[0]
                    distances = kmeans_model.transform(input_scaled)[0]
                    confidence = 1 - (distances[cluster] / np.sum(distances))
                    
                    results["customer_predictions"].append({
                        "sample_index": idx,
                        "cluster": int(cluster),
                        "cluster_meaning": CLUSTER_MEANINGS.get(cluster, f"Cluster {cluster}"),
                        "confidence": float(confidence)
                    })
                    
                except Exception as e:
                    results["customer_predictions"].append({
                        "sample_index": idx,
                        "error": str(e)
                    })
        return jsonify(results)
    
    except Exception as e:
        return jsonify({"error": f"Lỗi khi dự đoán batch: {str(e)}"}), 500

@app.route('/models/info', methods=['GET'])
def models_info():
    """
    ENDPOINT 6: Models Information - Thông tin về các models
    Method: GET
    Purpose: Trả về thông tin chi tiết về các models đã load
    """
    info = {
        "wine_quality": None,
        "customer_segmentation": None
    }
    
    if wine_model is not None:
        try:
            clf = wine_model.named_steps['clf']
            info["wine_quality"] = {
                "model_type": "RandomForestClassifier",
                "n_estimators": clf.n_estimators,   
                "features": WINE_FEATURES,
                "n_features": len(WINE_FEATURES),
                "classes": ["Bad (<6)", "Good (≥6)"]
            }
        except:
            info["wine_quality"] = {"status": "Loaded but info unavailable"}
    
    if kmeans_model is not None:
        info["customer_segmentation"] = {
            "model_type": "KMeans",
            "n_clusters": kmeans_model.n_clusters,
            "features": CUSTOMER_FEATURES,
            "n_features": len(CUSTOMER_FEATURES),
            "cluster_meanings": CLUSTER_MEANINGS
        }
    
    return jsonify(info)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Multi-Model Prediction API")
    print("="*60)
    print(f"Server running on: http://localhost:5000")
    print(f"Mobile/Web can access: http://<your-ip>:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
    
    