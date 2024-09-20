from flask import Flask, request, render_template, redirect, url_for
import tkinter as tk
from threading import Thread
import time
from asker import asker
from ip_catcher import get_router_ip
import time
import io
import mss
from PIL import Image
from flask import Flask, Response, render_template

import psutil
from screeninfo import get_monitors

# Get the primary monitor's width and height
monitor = get_monitors()[0]
width, height = monitor.width, monitor.height


app = Flask(__name__)

@app.route('/')
def req():
    return render_template('index.html')

@app.route('/txt', methods=['POST'])
def gets():
    t = request.form['txt']
    Thread(target=show_alert, args=[t]).start()
    return redirect(url_for('req'))

@app.route('/submit-file', methods = ['POST'])
def files():
    file = request.files['file']
    asker(file)
    return redirect(url_for('req'))

def capture_screen():
    with mss.mss() as sct:
        # Define the screen area to capture
        monitor = {"top": 0, "left": 0, "width": width, "height": height}

        while True:
            # Capture a screenshot
            img = sct.grab(monitor)

            # Convert the screenshot to PNG format
            img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
            buf = io.BytesIO()
            img.save(buf, format='JPEG')

            # Yield the PNG data as a stream response
            yield (b'--frame\r\n'
                   b'Content-Type: image/png\r\n\r\n' + buf.getvalue() + b'\r\n')

            # Wait for some time before capturing the next screenshot


@app.route('/see')
def index():
    return render_template('moz.html')

@app.route('/screen')
def stream_screen():
    return Response(capture_screen(), mimetype='multipart/x-mixed-replace; boundary=frame')



def generate_metrics():
    while True:
        # Get the CPU usage percentage
        cpu_percent = psutil.cpu_percent()

        # Get the memory usage percentage
        memory = psutil.virtual_memory()
        mem_percent = memory.percent

        # Get the disk usage percentage
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent

        # Yield the metrics as an SSE response
        yield 'data: {"cpu": %d, "memory": %d, "disk": %d}\n\n' % (cpu_percent, mem_percent, disk_percent)
        time.sleep(0.2)
        

@app.route('/metrics')
def metrics():
    return Response(generate_metrics(), mimetype='text/event-stream')

def show_alert(txt):

    def copy_text():
        text = txt
        root.clipboard_clear()
        root.clipboard_append(text)
        label.config(text="Text copied to clipboard!", fg="green")
        root.destroy()

    root = tk.Tk()
    root.title("Copy the text")
    root.geometry("400x200")
    root.config(bg="#202020")

    label = tk.Text(root, fg="#fff", bg="#202020", font=("Arial", 14))
    label.insert(tk.END, txt)
    label.pack(pady=20)

    button = tk.Button(root, text="Copy to Clipboard", command=copy_text, bg="#555", fg="#fff", font=("Arial", 12), padx=10, pady=5, borderwidth=0)
    button.pack(pady=10)

    root.mainloop()
print('System Ip:',get_router_ip())
app.run('0.0.0.0',port=1234,debug=False)