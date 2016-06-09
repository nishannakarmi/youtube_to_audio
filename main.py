from __future__ import unicode_literals
from flask import Flask, render_template, request, redirect, url_for
import youtube_dl
from utils import get_video_info
from settings import MAXIMUM_VIDEO_TIME, ERROR_MSG

app = Flask(__name__)
# app.run(debug=True)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pre_process', method=['POST'])
def pre_process():
    if request.method == 'POST':
        urls = request.form.getlist('url')
        if len(urls):
            for url in urls:
                info = get_video_info(url)
                if info:
                    pass
                else:
                    pass


@app.route('/process', methods=['POST'])
def process_file():
    status = {}
    if request.method == 'POST':
        print request.form.getlist('url')
        urls = request.form.getlist('url')
        if len(urls):
            counter = 0
            for url in urls:
                counter += 1
                info = get_video_info(url)
                status[counter] = {'success': False}
                if info:
                    status[counter]['title'] = info['title'] if 'title' in info else ''
                    if info['duration'] <= MAXIMUM_VIDEO_TIME:
                        download_url = [url]
                        ydl_opts = {
                            'format': 'bestaudio/best',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                            'outtmpl': 'tmp/%(title)s-%(id)s.%(ext)s',
                        }
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            ydl.download(download_url)
                            status[counter]['success'] = True
                    else:
                        if info['duration'] > 360:
                            status[counter]['msg'] = ERROR_MSG['MAX_VIDEO_TIME']
                else:
                    status['counter']['msg'] = ERROR_MSG['UNKNOWN']
                print status

            return render_template('process_file.html')

    return redirect(url_for('home'))


@app.route('/download')
def download():
    return render_template('download.html')
