# app_abj_backend
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
pip install -r requirements.txt
.\venv\Scripts\Activate  
uvicorn main:app --reload
