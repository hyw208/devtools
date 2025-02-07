FROM python:3.12.9

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY devtools devtools

CMD ["python", "devtools/api.py"]