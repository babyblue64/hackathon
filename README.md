## Setup instructions

# Frontend

* Get into 'frontend' using 

```bash
cd frontend
```

* Then run:

```bash
npm install
npm run dev
```

# Backend

* Get into 'backend' using

```bash
cd backend
```

* Then run:

```bash
python2 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --port 8000
```