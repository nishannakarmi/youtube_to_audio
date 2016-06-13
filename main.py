from __future__ import unicode_literals
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
import youtube_dl
from utils import get_video_info
from settings import MAXIMUM_VIDEO_TIME, ERROR_MSG, SECRET_KEY, MAXIMUM_NUMBER_OF_VIDEOS, TMP_DIR
import uuid
import os
import zipfile

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
            msg = 'Something went wrong while converting'
            custom_dirs = TMP_DIR + custom_uuid
            if not os.path.exists(custom_dirs):
                os.makedirs(custom_dirs)

            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': '{custom_dirs}/%(title)s.%(ext)s' .format(custom_dirs=custom_dirs),
            }

            for url in session.get('urls'):
                download_url = [url]
                try:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download(download_url)
                except Exception:
                    success = False
            if success:
                for fname in os.listdir(custom_dirs):
                    links.append('%s' %(str(fname)))
                msg = "Conversion successful"

        else:
            msg = ERROR_MSG['UNKNOWN']

        return jsonify(success=success, custom_uuid=custom_uuid, msg=msg, links=links)
    else:
        flash("Unauthorized access")
        return redirect(url_for('home'))


@app.route('/download')
def download():
    if request.args.get('fname') and request.args.get('custom_uuid'):
        # return send_file(request.args.get('url'), filename_or_fp="a.mp3")
        custom_dirs = '%s%s' %(TMP_DIR, str(request.args.get('custom_uuid')))
        return send_from_directory(directory=custom_dirs, filename=str(request.args.get('fname')), as_attachment=True)
    else:
        flash(ERROR_MSG['UNKNOWN'])
        return redirect(url_for('home'))


@app.route('/download_zip')
def download_zip():
    custom_uuid = request.args.get('custom_uuid')
    if custom_uuid:
        zf = zipfile.ZipFile('%s%s.zip' %(TMP_DIR, custom_uuid), "w")
        for dirname, subdirs, files in os.walk('%s%s' %(TMP_DIR, custom_uuid)):
            zf.write(dirname)
            for filename in files:
                zf.write(os.path.join(dirname, filename))
        zf.close()
        return send_from_directory(directory=TMP_DIR, filename='%s.zip' %custom_uuid, as_attachment=True)
    else:
        flash(ERROR_MSG['UNKNOWN'])
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()