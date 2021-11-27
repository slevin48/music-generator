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


# 2 modes: youtube URL or search
src = st.radio("Youtube URL or Search",["Youtube URL","Youtube Search"])



if src == "Youtube URL":

    # Indie/Pop/Folk Compilation - December 2021
    # url = 'https://www.youtube.com/watch?v=6no3uMeMIr8'
    # One Repubilc - Someday
    # url = "https://www.youtube.com/watch?v=vNfgVjZF8_4" 
    # Jason Derulo - Savage Love
    url = "https://www.youtube.com/watch?v=sQR2-Q-k_9Y"
    url = st.text_input('Youtube URL',url)
    # Download Youtube video
    youtube = pytube.YouTube(url)
    videos = youtube.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')
    # l = [s.resolution + " (" + str(round(s.filesize/2**10/2**10)) + " MB)" for s in videos]
    # i = st.radio("Select resolution",range(len(videos)),format_func = lambda x: l[x])
    # video = videos[i]
    video = videos.first() 
    
else:

    search = st.text_input('Youtube Search',"jason derulo savage love")
    r = pytube.Search(search).results
    # st.write(r[0].streams.first().title)
    # t = [i.streams.first().title for i in r]
    # st.radio("Search results",t)
    video = r[0].streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

dl = st.button('Download')

if dl:
    
    st.write(video)
    title = video.title
    path = video.download('downloads')
    st.markdown("["+title+"]("+video.url+")")
    st.video(path,format='video/mp4', start_time=0)

    try:
        my_clip = mp.VideoFileClip(path)
        duration = int(my_clip.duration)
        minutes, seconds = divmod(duration, 60)

        # Video to Audio
        my_clip.audio.write_audiofile("downloads/music.mp3")
        st.text("Duration: "+format_time(duration))
        st.audio("downloads/music.mp3", format='audio/mp3')
        with open("downloads/music.mp3", "rb") as file:
            st.download_button("Download music",data=file,file_name=title+".mp3")

    except NameError:
        print('No video to process')