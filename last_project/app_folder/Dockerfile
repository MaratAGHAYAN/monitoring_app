FROM python:3.11.5

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP app.py

CMD ["python", "app.py"]
