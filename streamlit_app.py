import streamlit as st
import pytube
import moviepy.editor as mp
import os
from datetime import date, datetime, time, timedelta

def format_time(d):
    
    dt = datetime.combine(date.today(), time(0, 0)) + timedelta(seconds=d)
    return "%02d:%02d:%02d" % (dt.hour,dt.minute,dt.second)


try:
    os.mkdir('downloads')
except OSError as error:
    print(error)

st.title('Music Generator📻')

url = 'https://www.youtube.com/watch?v=6no3uMeMIr8'

url = st.text_input('Youtube URL',url)

# Download Youtube video
youtube = pytube.YouTube(url)
videos = youtube.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')
# l = [s.resolution + " (" + str(round(s.filesize/2**10/2**10)) + " MB)" for s in videos]
# i = st.radio("Select resolution",range(len(videos)),format_func = lambda x: l[x])
# video = videos[i]
video = videos.first()
dl = st.button('Download')

if dl:   
    st.write(video)
    title = video.title
    path = video.download('downloads')
    st.text(title)
    st.video(path,format='video/mp4', start_time=0)

    try:
        my_clip = mp.VideoFileClip(path)
        duration = int(my_clip.duration)
        minutes, seconds = divmod(duration, 60)

        # Video to Audio
        my_clip.audio.write_audiofile("downloads/music.mp3")
        st.text("Duration: "+format_time(duration))
        st.audio("downloads/music.mp3", format='audio/mp3')

    except NameError:
        print('No video to process')