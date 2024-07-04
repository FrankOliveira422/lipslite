from flask import Flask, request, render_template, redirect, url_for
import youtube_dl
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_type = request.form['format']

    # Define opções para youtube-dl
    ydl_opts = {}
    if format_type == 'mp4':
        ydl_opts = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4'}
    elif format_type == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        return "Formato inválido!"

    try:
        # Baixa o vídeo com youtube-dl
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info_dict)
            ydl.download([url])
            download_path = os.path.join(os.path.expanduser('~'), 'Downloads')
            final_path = os.path.join(download_path, os.path.basename(filename))
            os.rename(filename, final_path)

        return f"Download concluído! Arquivo salvo em: {final_path}"
    except Exception as e:
        return f"Erro ao baixar o vídeo: {e}"

if __name__ == '__main__':
    app.run(debug=True)
