from flask import Flask, request, render_template, redirect, url_for
import pytube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    video = pytube.YouTube(url)

    # Escolher o formato do arquivo (MP4 ou MP3)
    format_type = request.form['format']

    if format_type == 'mp4':
        stream = video.streams.get_highest_resolution()
        filename = f"{video.title}.mp4"
    elif format_type == 'mp3':
        stream = video.streams.filter(only_audio=True).first()
        filename = f"{video.title}.mp3"
    else:
        return "Formato inválido!"

    # Obter o caminho da pasta de downloads do usuário
    download_path = os.path.join(os.path.expanduser('~'), 'Downloads')

    # Realizar o download
    stream.download(output_path=download_path, filename=filename)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
