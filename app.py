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
    url = request.form['url']
    try:
        video = pytube.YouTube(url)
        time.sleep(2)  # Adicionar uma pausa de 2 segundos entre requisições

        format_type = request.form['format']

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
        
    except pytube.exceptions.RegexMatchError as e:
        return f"Erro ao processar a URL: {str(e)}"
    except pytube.exceptions.VideoUnavailable:
        return "Vídeo não disponível."
    except Exception as e:
        return f"Ocorreu um erro ao baixar o vídeo: {str(e)}"

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
