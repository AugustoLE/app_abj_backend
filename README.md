# app_abj_backend
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
python -m venv venv
pip install -r requirements.txt
.\venv\Scripts\Activate  
uvicorn main:app --reload
