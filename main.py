import streamlit as st
import subprocess
from subprocess import Popen,PIPE
import ffmpeg

import soundfile as sf
import librosa
import time
import threading
import scipy.io.wavfile as wavfile
import os
import signal
from streamlink import Streamlink
import whisper
import itertools

import datetime




st.set_page_config(layout="wide")
model=whisper.load_model('large-v3')
audio_value = st.audio_input("Record a voice message")

if audio_value:
    st.audio(audio_value)
url = st.sidebar.text_input(':blue[Add Live youtube URL here:]')
def stream_to_url(url, quality='worst'):
    # The "audio_only" quality may be invalid for some streams (check).
    session = Streamlink()
    streams = session.streams(url)
    return streams[quality].to_url()


#class Record:
    #def __init__(self):
        #self.ffmpeg_process = None
d=[]

def audiocli():
    os.makedirs('temp', exist_ok=True)
    process= subprocess.Popen( ["streamlink" , url ,
                                "worst", "-o",'temp/recording.wav'])
    st.write('recording started')
    def Finish():

        process.send_signal(signal.SIGQUIT)
        st.write(':red[Recording FINISHED ..... ]',height=30)
        st.audio('temp/recording.wav')
        st.text_area(label=' Transcript : ', value= d ,height=200)
    st.sidebar.button("Finish Recording ",on_click=Finish)

    
def oneFunction():
    os.makedirs('temp', exist_ok=True)
    stream_url = stream_to_url(url)
    fmpeg_process = (ffmpeg
.input(stream_url)
.audio
.output('temp/recording.wav')
.overwrite_output()
.run_async())
    st.write(":red[RECORDING Audio ....]",height=30)
    def Finish():

        fmpeg_process.send_signal(signal.SIGQUIT)
        st.write(':red[Recording FINISHED ..... ]',height=30)
        st.audio('temp/recording.wav')
        st.text_area(label=' Transcript : ', value= d ,height=200)

    st.sidebar.button("Finish Recording ",on_click=Finish)

        #play_audio=st.audio("/content/recording.wav")
        #st.text_area(label=' Transcript : ', value= text ,height=200)
        #ffmpeg_process.send_signal(signal.CTRL_C_EVENT)




def done():

    lasttimeinterval=0


    for i in itertools.count():
        audio_array, sr = librosa.load("temp/recording.wav", sr=16_000)
        timeinterval=len(audio_array)/sr
        t=audio_array[int(lasttimeinterval)*sr : int(timeinterval)*sr]
        sf.write("temp/split_interval.wav", t, sr)
        result=model.transcribe("temp/split_interval.wav" )
        if result['text']:

            #translated = GoogleTranslator(source='auto', target='en').translate(result['text'])

            yield str(datetime.timedelta(seconds=int(lasttimeinterval))) , result['text'] #st.text_area(label=' Transcript : ', value= result['text'] ,height=200)
            d.append(result['text'])
        yield "\n"
        #yield translated
        #with col2:
                #yield st.write_stream(translated)

        lasttimeinterval=timeinterval





    #st.text_area(label=' Translation : ', value= translation,height=200)
if url :
    play_file=st.sidebar.video(url)
record=st.sidebar.button(":blue[Record Audio and transcribe  ]" ,use_container_width=True)
record1=st.sidebar.button(":blue[Record Audio and transcribe CLI   ]" ,use_container_width=True)
transcribe=st.sidebar.button(":blue[ live  Transcribe  ]" ,use_container_width=True)
#stop=st.sidebar.button(":blue[Stop  ]" ,use_container_width=True)
if st.sidebar.button("Play Recorded Audio"):
    st.write("Recorded File  " )
    video_file = open('temp/recording.wav', "rb")
    video_bytes = video_file.read()
    st.audio(video_bytes)


if st.sidebar.button('show transcription :'):
    st.text_area(label=' Transcript : ', value= d ,height=200)
if record :


    oneFunction()
    #done
    #recorder.start_recording(url)
if record1 :
    audiocli()

        #oneFunction.stop(fmpeg_process)
if transcribe:
  done
#stop=st.sidebar.button(":blue[Stop  ]" ,use_container_width=True)
#if stop:
  #recorder.stop_recording()
#if stop :
    #b.stop_recording()





    #stop=st.sidebar.button(":blue[Stop  ]" ,use_container_width=True)
    #if stop :
        #p1.join(1)
        #fmpeg_process.send_signal(signal.SIGINT)
