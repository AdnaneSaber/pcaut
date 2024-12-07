from flask import Flask, send_file, redirect, url_for, abort
import os
from langdetect import detect
import requests

app = Flask(__name__)

@app.route('/')
def redirect_to_new_path():
    secret_value = os.getenv('LINK_TO_ASSET')
    print(secret_value)
    return redirect(secret_value)


GITHUB_REPO = 'AdnaneSaber/pcaut'
GITHUB_RELEASE_TAG = 'test_release'
FILE_NAME = '3S_PC_automation.exe'
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# GitHub API URL for the release assets
GITHUB_API_URL = f'https://api.github.com/repos/{GITHUB_REPO}/releases/tags/{GITHUB_RELEASE_TAG}'



@app.route('/download')
def download_file():
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    
    # Fetch release information
    response = requests.get(GITHUB_API_URL, headers=headers)
    if response.status_code != 200:
        abort(404, description='Release not found or authentication failed')

    release_info = response.json()
    assets = release_info.get('assets', [])

    # Find the asset with the specified file name
    asset_url = None
    for asset in assets:
        if asset['name'] == FILE_NAME:
            asset_url = asset['browser_download_url']
            break
    
    if asset_url is None:
        abort(404, description='File not found in release')

    # Download the file
    file_response = requests.get(asset_url, headers=headers)
    if file_response.status_code != 200:
        abort(404, description='Failed to download file')

    # Return the file as a response
    return send_file(
        BytesIO(file_response.content),
        attachment_filename=FILE_NAME,
        as_attachment=True
    )


@app.route('/weather', methods=['POST'])
def get_weather():
    # Get the query from the request JSON
    data = request.get_json()
    query = data.get('question')
    
    if not query:
        return jsonify({"error": "No question provided"}), 400

    # Detect the language of the query
    language = detect(query)
    
    # Based on the detected language, route to the appropriate assistant
    if language == 'en':  # English
        city, day = weather_en.extract_city_and_day(query)
    elif language == 'ko':  # Korean
        city, day = weather_kr.extract_city_and_day(query)
    else:
        return jsonify({"error": "Unsupported language"}), 400

    # Return the response as JSON
    return jsonify({"city": city, "day": day})