from flask import Flask, request, render_template, redirect, url_for
import pytube
import os
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.form['url']
        video = pytube.YouTube(url)
        time.sleep(2)  # Espera de 2 segundos para reduzir o risco de sobrecarga

        format_type = request.form['format']
        if format_type == 'mp4':
            stream = video.streams.get_highest_resolution()
            filename = f"{video.title}.mp4"
        elif format_type == 'mp3':
            stream = video.streams.filter(only_audio=True).first()
            filename = f"{video.title}.mp3"
        else:
            return "Formato inválido!"

        download_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        stream.download(output_path=download_path, filename=filename)

    except pytube.exceptions.PytubeError as e:
        return f"Erro ao baixar o vídeo: {e}"
    except Exception as e:
        return f"Erro inesperado: {e}"

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
