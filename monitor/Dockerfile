FROM python:3.8-slim

WORKDIR /app

COPY monitor.py .

RUN pip install pika psutil

CMD ["python", "monitor.py"]
