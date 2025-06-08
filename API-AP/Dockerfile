FROM python:3.9-slim

WORKDIR /API-AP

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /API-AP

CMD ["gunicorn", "-w", "1", "--threads", "4", "-k", "gthread", "-b", "0.0.0.0:8010", "api_ap:app"]