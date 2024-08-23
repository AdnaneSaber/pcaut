from flask import Flask, send_file, redirect, url_for
import os

app = Flask(__name__)

@app.route('/download')
def download():
    file_path = "../dist/3S_PC_automation.exe"
    return send_file(file_path, as_attachment=True, download_name='3S_PC_automation.exe')


@app.route('/')
def redirect_to_new_path():
    secret_value = os.getenv('LINK_TO_ASSET')
    return redirect(secret_value)

@app.route('/test')
def test():
    return 'Hello world'
