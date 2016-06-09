import youtube_dl


def get_video_info(url):
    if url:
        ydl = youtube_dl.YoutubeDL()
        ydl.add_default_info_extractors()
        try:
            return ydl.extract_info(url, download=False)
        except youtube_dl.DownloadError:
            return None

    return None