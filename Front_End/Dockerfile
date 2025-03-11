FROM python:3.9-slim

WORKDIR /Front_End

COPY requirements.txt requirements.txt 
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

EXPOSE 80

CMD ["python", "FE_app.py"]

