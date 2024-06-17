from flask import Flask, render_template, request
import psutil
import threading
import time
from queue import Queue

app = Flask(__name__)

metrics_queue = Queue()

def monitor_system():
    while True:
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        
        metrics_queue.put((cpu_usage, memory_usage, disk_usage))
        
        time.sleep(1)

monitor_thread = threading.Thread(target=monitor_system, daemon=True)
monitor_thread.start()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cpu = request.form['cpu']
        ram = request.form['ram']
        return render_template('index.html', cpu=cpu, ram=ram, submitted=True)
    
    if not metrics_queue.empty():
        cpu_usage, memory_usage, disk_usage = metrics_queue.get()
    else:
        cpu_usage, memory_usage, disk_usage = 0, 0, 0
    
    return render_template('index.html', cpu_usage=cpu_usage, memory_usage=memory_usage, disk_usage=disk_usage, submitted=False)

if __name__ == '__main__':
    app.run(debug=True)
