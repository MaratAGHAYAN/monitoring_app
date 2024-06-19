
import time
import psutil
import pika
import json

def get_system_metrics():
    return {
        'cpu': psutil.cpu_percent(interval=1),
        'ram': psutil.virtual_memory().percent,
    }

def send_metrics_to_queue():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('queue'))
            channel = connection.channel()
            channel.queue_declare(queue='metrics')
            break
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ not ready, retrying in 5 seconds...")
            time.sleep(5)
    
    while True:
        metrics = get_system_metrics()
        message = json.dumps(metrics)
        channel.basic_publish(exchange='', routing_key='metrics', body=message)
        time.sleep(5)

if __name__ == "__main__":
    send_metrics_to_queue()
