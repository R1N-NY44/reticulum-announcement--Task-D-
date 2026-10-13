
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV RETICULUM_CONFIG=/reticulum

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY node_a.py node_b.py ./

RUN mkdir -p /reticulum

CMD ["python", "node_b.py"]
