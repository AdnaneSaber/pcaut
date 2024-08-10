from flask import Flask, send_file, redirect, url_for

app = Flask(__name__)

@app.route('/download')
def download():
    file_path = "../3S_PC_automation.exe"
    return send_file(file_path, as_attachment=True, download_name='3S_PC_automation.exe')


@app.route('/')
def redirect_to_new_path():
    return redirect('https://drive.usercontent.google.com/download?id=1FAiXV-s-LBcNAvGegI8aMPXOWe5_KHX7&export=download')
