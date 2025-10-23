step-to-step activate venv:

S1: python -m venv venv </br>
S2: python -m pip install --upgrade pip </br>
S3: pip install requirements.txt  </br>
S4: OK

git rm -r --cached venv


# todo list run server
## 1. Kiểm tra server đang chạy
netstat -ano | findstr :8000
## 2. Khởi động Uvicorn
uvicorn app:app --host 127.0.0.1 --port 8000
