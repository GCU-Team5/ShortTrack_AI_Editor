import os
import json
import io
from google.cloud import storage
from google.cloud import speech
from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt
import moviepy.editor as mp


def Frequency_score(up_frequency, count, point):  #주파수 스코어  각각 키워드 추출시간, 영상Frame 길이, point점수
    
    score=[0 for i in range(count)]     #
   
    for i in up_frequency:
        frame_index = i/1
        frame_index = round(frame_index)
        score[frame_index] = point
  
    return score


def keyword_detection(word_time, count, point):    #STT 스코어  각각 키워드 추출시간, 영상Frame 길이, point점수

    score=[0 for i in range(count)]
    
    for i in word_time:
        frame_index = i/1
        frame_index = round(frame_index)
        score[frame_index] = point

    return score

    
def STT_detection(count,path):
    clip = mp.VideoFileClip(path)  #처음 wav파일로 바꿀 mp4파일 것
    clip.audio.write_audiofile("audio.wav")    #저장할 wav파일 이름 설정


    sample_rate, data = wavfile.read('audio.wav') #저장한 wav파일을 읽음
    arr1, arr2 = np.split(data, 2, axis=1)

    time = np.linspace(0, len(data) / sample_rate, len(data))


    times = np.arange(len(data)) / sample_rate
    up_frequency = times[np.argwhere(np.squeeze(arr2) >= 28000)].squeeze() #주파수 28000이상 저장

    for i in range(len(up_frequency)):  #int형으로 변환
        up_frequency[i] = int(up_frequency[i])

        
    up_frequency = list(set(up_frequency))

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"google_json\pure-anthem-369402-9bcdbdacbb25.json"

    client = speech.SpeechClient()

    storage_client = storage.Client()
    buckets = list(storage_client.list_buckets())



    bucket_name = 'short_track-ai_editor'  # 서비스 계정 생성한 bucket 이름 입력
    source_file_name = r'audio.wav'  # GCP에 업로드할 파일 경로
    destination_blob_name = 'audio.wav'  # 업로드할 파일을 GCP에 저장할 때의 이름

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name) 

    blob.upload_from_filename(source_file_name)


    word_time = [] #키워드 시간초 저장
    word_time2 = []
    word_time3 = []

    keyword = ["일본", "중국", "랭킹" ]                 #키워드 3점  
    keyword2 = ["가고", "도움", "밀어", "잡아당겼"]     #5점
    keyword3 = ["출발", "충돌", "마지막", "추월", "넘어졌", "넘어짐"]   #10점

    def transcribe_gcs(gcs_uri):
        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(uri=gcs_uri)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code='ko-KR',
            enable_word_time_offsets=True,
            audio_channel_count=2)
        operation = client.long_running_recognize(request={"config": config, "audio": audio})
        response = operation.result()



        for result in response.results:
            alternative = result.alternatives[0]
            for word_info in alternative.words:
                word = word_info.word
                start_time = word_info.start_time.total_seconds()
            

                if word_info.word in keyword:               #키워드 나오는 시간 List에 추가
                    word_time.append(start_time)
                
                elif word_info.word in keyword2:
                    word_time2.append(start_time)

                elif word_info.word in keyword3:
                    word_time3.append(start_time)
                
                
        
        return response



    response = transcribe_gcs("gs://short_track-ai_editor/audio.wav") # 구글 안에 있는 STT 파일이라서 바꾸면 안될듯




    #print("단어나오는 시간")
    #print(word_time)

    #print("주파수 28000이상")
    #print(up_frequency)


    frame_len=count

    score = keyword_detection(word_time, frame_len, 3)   #STT 스코어  각각 키워드 추출시간, 영상Frame 길이, Score점수
    score2 = keyword_detection(word_time2, frame_len, 5)   
    score3 = keyword_detection(word_time3, frame_len, 10)   
    score4 = Frequency_score(up_frequency, frame_len, 1) #주파수 스코어 

    total_score = [score[i] + score2[i] + score3[i] + score4[i] for i in range(len(score))] # 스코어들의 List 합

    print("STT_score:", total_score)

    return total_score