FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 50052

ENV PYTHONUNBUFFERED=1

CMD ["python", "server.py"]
