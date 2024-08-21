from flask import Flask, send_file, redirect, url_for

app = Flask(__name__)

@app.route('/download')
def download():
    file_path = "../dist/3S_PC_automation.exe"
    return send_file(file_path, as_attachment=True, download_name='3S_PC_automation.exe')


@app.route('/')
def redirect_to_new_path():
    return redirect('https://raw.githubusercontent.com/AdnaneSaber/pcaut/main/3S_PC_automation.exe')

@app.route('/test')
def redirect_to_new_path():
    return 'Hello world'
