import pafy
import os
from pydub import AudioSegment
import time
import datetime


def download_audio(video_id, video_url):
    if not video_id:
        return {"status": False, "error": "Video id not specified"}

    try:
        video = pafy.new(str(video_url))
    except ValueError as e:
        print(e)
        return {"status": False, "error": "Invalid video id specified"}
    
    path = get_song(video.title)

    if path:
        return {"status": True, "path": path, "duration": get_duration(video.duration), "title": video.title} 


    streams = video.audiostreams
    if len(streams) > 0:
        filename = video.getbestaudio().download(filepath="./dist", quiet=True)
        convert_to_mp3(filename, video.title)
        os.remove(filename)
        file_path = "./dist/%s.mp3" % video.title
        return {"status": True, "path": file_path, "duration": get_duration(video.duration), "title": video.title} 

    return {"status": False, "error": "No audio streams found"}



def get_song(title):
    path = './dist/' + title + '.mp3'
    if(os.path.exists(path)):
        return path
    
    return None

def convert_to_mp3(path, title):
    AudioSegment.from_file(path).export("./dist/" + title + ".mp3", format="mp3")

def get_duration(time_str):
	x = time.strptime(time_str, "%H:%M:%S")
	return datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()

