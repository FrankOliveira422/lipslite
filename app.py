from flask import Flask, request, render_template, redirect, url_for, flash
from pytube import YouTube
import os
import time
import urllib.error
import logging

app = Flask(__name__)
app.secret_key = 'secret_key_for_session'  # Necessário para usar flash messages

# Configurar logs
logging.basicConfig(level=logging.INFO)

def download_video(url, format_type, max_retries=3):
    retry_delay = 5  # Segundos de espera inicial entre retentativas
    retries = 0
    while retries < max_retries:
        try:
            video = YouTube(url)
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
                logging.warning(f"Erro 429: Tentativa {retries + 1}. Esperando {retry_delay} segundos.")
                if retries < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Aumenta o tempo de espera exponencialmente
                    retries += 1
                else:
                    logging.error("Limite de retentativas atingido.")
                    return "Limite de retentativas atingido. Tente novamente mais tarde."
            else:
                logging.error(f"Erro HTTP {e.code}: {str(e)}")
                return f"Erro HTTP {e.code}: {str(e)}"
        except Exception as e:
            logging.error(f"Ocorreu um erro ao baixar o vídeo: {str(e)}")
            return f"Ocorreu um erro ao baixar o vídeo: {str(e)}"
    return "Limite de retentativas atingido. Tente novamente mais tarde."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_type = request.form['format']
    error_message = download_video(url, format_type)
    if error_message:
        flash(error_message)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
