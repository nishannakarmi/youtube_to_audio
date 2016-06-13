# youtube_to_audio
Web application to convert youtube video to audio file

INSTALLATION GUIDE (Assuming linux {ubuntu} environment)
- Python version 2.7.*
- ffmpeg module should be installed if not, install as $ sudo apt-get install ffmpeg
- pip (python package manager should be installed)
- Install python additional packages as $ sudo pip install -r requirements.txt
- If all of the above package installed successfully, then we start it as
    $ python main.py

- Default video file time has been set to 6 min. ie. we cannot download videos having time more than 6 min.
    To change it change the value of MAXIMUM_VIDEO_TIME in setting.py. It should be in seconds.
- A python script file (remove_old_files.py) has been added. Place it in cron tab to run once a day as:
    $ python remove_old_files.py
    It checks files/folder older than 1 day (today) if know any, it removes all found files/folder.
