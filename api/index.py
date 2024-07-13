from flask import Flask, send_file

app = Flask(__name__)

@app.route('/')
def home():
    file_path = "../3S_PC_automation.exe"
    return send_file(file_path, as_attachment=True, download_name='3S_PC_automation.exe')
