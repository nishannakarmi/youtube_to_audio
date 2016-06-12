from __future__ import unicode_literals
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import youtube_dl
from utils import get_video_info
from settings import MAXIMUM_VIDEO_TIME, ERROR_MSG, SECRET_KEY, MAXIMUM_NUMBER_OF_VIDEOS, TMP_DIR
import uuid

app = Flask(__name__)
app.debug = True
app.secret_key = SECRET_KEY


@app.route('/')
def home():
    return render_template('index.html', max_videos=MAXIMUM_NUMBER_OF_VIDEOS)


@app.route('/pre_process', methods=['POST'])
def pre_process():
    if request.method == 'POST':
        urls = request.form.getlist('url')
        custom_uuid = None
        if len(urls):
            error_msg = []
            video_titles = []
            for url in urls:
                info = get_video_info(url)
                print(info['title'])
                if info and info['duration'] <= MAXIMUM_VIDEO_TIME:
                    video_titles.append(info['title'])
                    continue
                else:
                    if not info:
                        error_msg.append(ERROR_MSG['UNKNOWN'])
                    else:
                        error_msg.append(ERROR_MSG['MAX_VIDEO_TIME'])
            if len(error_msg):
                flash("\n".join(error_msg))
                return redirect(url_for('home'))
            else:
                custom_uuid = uuid.uuid4()
                session['urls'] = urls
                session['uuid'] = custom_uuid
                session['video_titles'] = video_titles
        else:
            flash("Please insert youtube video url's")
            return redirect(url_for('home'))
        return render_template('pre_process.html', custom_uuid=custom_uuid)


@app.route('/process', methods=['POST'])
def process_file():
    if request.method == 'POST':
        custom_uuid = request.form['custom_uuid']
        success = False
        links = []

        if custom_uuid and (str(custom_uuid) == str(session.get('uuid', None))):
            success = True
            msg = 'It Works Cheers!'
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': 'tmp/%(title)s-%(id)s.%(ext)s',
            }

            for url in session.get('urls'):
                download_url = [url]
                try:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download(download_url)
                except Exception:
                    success = False
            if success:
                for title in session.get('video_titles'):
                    links.append('%s%s/%s' %(TMP_DIR, str(custom_uuid), str(title)))
                msg = "It Works and downloaded, Check download folder %s" %(str(custom_uuid))

        else:
            msg = ERROR_MSG['UNKNOWN']

        return jsonify(success=success, custom_uuid=custom_uuid, msg=msg, links=links)
    else:
        flash("Unauthorized access")
        return redirect(url_for('home'))


@app.route('/download')
def download():
    return render_template('download.html')


if __name__ == '__main__':
    app.run()