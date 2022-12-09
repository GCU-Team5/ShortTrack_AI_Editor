import os
import json
import io
from google.cloud import storage
from google.cloud import speech
from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt
import moviepy.editor as mp


def Frequency_score(up_frequency, count, point, xg_list):  #주파수 스코어  각각 키워드 추출시간, 영상Frame 길이, point점수
    
    score=[0 for i in range(count)]     #
   
    for i in up_frequency:
        frame_index = i/1
        frame_index = round(frame_index)
        xg_list[frame_index][1]=1
        score[frame_index] = point
  
    return score


def keyword_detection(word_time, count, point, xg_list):    #STT 스코어  각각 키워드 추출시간, 영상Frame 길이, point점수

    score=[0 for i in range(count)]
    
    for i in word_time:
        frame_index = i/1
        frame_index = round(frame_index)
        xg_list[frame_index][0]=1
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

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"google_json/pure-anthem-369402-9bcdbdacbb25.json"

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

    keyword = [ "랭킹","조심","엉키는", "의식", "찬스","인코스", "자리", "연결", "첫번째 주자", "선두", "결승전", "가장먼저", "1번주자"
            "안전하게" ] 
                #키워드 3점  
    keyword2 = [ "가고", "결과" "도움", "마킹", "밀어", "잡아당겼","빠르게", "에이스", "추격", "출발합니다"
            "좋아", "좋습니다", "넘겨줍니다", "타이밍"," 추격", "두바퀴", "바톤을", "경기초반", "거리를", "1위", "2위", "치고 나갑니다."]     #5점

    keyword3 = ["출발", "충돌", "마지막", "추월", "넘어졌습니다", "대한민국 에이스" "넘어짐", "파이널", "결승선 통과", "부딪", "레디", "스타트", 
                 "한바퀴", "마지막 주자", "파이널랩", "결승진출","뻗습니다.", "미끄러", "결승진출", "마지막 코너"]   #10점

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
    xg_list=[[0]*2 for _ in range(frame_len)]
    
    score = keyword_detection(word_time, frame_len, 1,xg_list)   #STT 스코어  각각 키워드 추출시간, 영상Frame 길이, Score점수
    score2 = keyword_detection(word_time2, frame_len, 3,xg_list)   
    score3 = keyword_detection(word_time3, frame_len, 5,xg_list)   
    score4 = Frequency_score(up_frequency, frame_len, 1,xg_list) #주파수 스코어 

    total_score = [score[i] + score2[i] + score3[i] + score4[i] for i in range(len(score))] # 스코어들의 List 합

    print("STT_score:", total_score)

    return total_score,xg_list