# Finance Api

## Installation
This api requires [Python](https://www.python.org/downloads/release/python-3100/) v3.10 and [MySQL](https://www.mysql.com/) server up to run.

#### Windows
Create virtual environment, install the dependencies and start the server.
```console
cd finance_api
python -m venv venv
venv\Scripts\activate
cd app
pip install -r requirements.txt
```
Add database connection string to .env file.
```console
uvicorn main:app --port 8080
```

## Docs
After server is up just go to http://localhost:8080/docs to see the docs.
