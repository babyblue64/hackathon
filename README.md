# Setup instructions

* Get into 'backend' directory using

```bash
cd backend
```

* Then run, one after the other:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --port 8000
```