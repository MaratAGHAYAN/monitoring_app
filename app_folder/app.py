from flask import Flask, render_template, request
import pika
import threading
import json
import time

app = Flask(__name__)

metrics = {'cpu': 0, 'ram': 0}


def consume_metrics():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters
                                                 ('localhost'))
            channel = connection.channel()
            channel.queue_declare(queue='metrics')

            def callback(ch, method, properties, body):
                global metrics
                metrics = json.loads(body)
                print(f"Received metrics: {metrics}")

            channel.basic_consume(queue='metrics',
                                  on_message_callback=callback, auto_ack=True)
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ not ready, retrying in 5 seconds...")
            time.sleep(5)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cpu = request.form['cpu']
        ram = request.form['ram']
        return render_template('index.html', cpu=cpu, ram=ram, submitted=True)

    return render_template('index.html', cpu_usage=metrics['cpu'],
                           memory_usage=metrics['ram'], submitted=False)


if __name__ == '__main__':
    threading.Thread(target=consume_metrics, daemon=True).start()
    app.run(debug=True, host='0.0.0.0', port=5000)
