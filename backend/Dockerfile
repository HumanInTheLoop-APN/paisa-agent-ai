FROM python:3.13-slim

WORKDIR /app

#install tk python
RUN apt-get update && apt-get install -y python3-tk tk-dev tk
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers", "--forwarded-allow-ips", "*"]