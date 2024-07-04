from flask import Flask, request, render_template, redirect, url_for
import pytube
import os
import time
import urllib

app = Flask(__name__)

def download_video(url, format_type, retries=3):
    while retries > 0:
        try:
            video = pytube.YouTube(url)
            if format_type == 'mp4':
                stream = video.streams.get_highest_resolution()
                filename = f"{video.title}.mp4"
            elif format_type == 'mp3':
                stream = video.streams.filter(only_audio=True).first()
                filename = f"{video.title}.mp3"
            else:
                return "Formato inválido!"

            download_path = os.path.join(os.path.expanduser("~"), "Downloads")
            if not os.path.exists(download_path):
                os.makedirs(download_path)
            stream.download(output_path=download_path, filename=filename)
            return None
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(5)  # Aumentar o tempo de espera em cada retentativa
                retries -= 1
            else:
                return f"Ocorreu um erro ao baixar o vídeo: {str(e)}"
    return "Limite de retentativas atingido."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_type = request.form['format']
    error_message = download_video(url, format_type)
    if error_message:
        return error_message
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
