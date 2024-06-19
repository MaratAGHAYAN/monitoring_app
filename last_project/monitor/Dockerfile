FROM python:3.8-slim

RUN pip install pika psutil

WORKDIR /app
COPY monitor.py .

CMD ["python", "monitor.py"]
