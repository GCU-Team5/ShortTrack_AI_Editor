import shutil
from turtle import width
from moviepy.editor import *

def frame_merge(video,total_score,start,sin,finish):
    #하이라이트 갯수
    max_highlight=3
    max_highlight_score = 8
    highlight = []
    highlight_position = []
    Start = VideoFileClip(start).subclip(0,1)
    Sin=VideoFileClip(sin)
    Sin=Sin.crossfadeout(1) #fadein 1초

    Finish=VideoFileClip(finish).subclip(0,1)
    
    #하이라이트 스코어가 일정 수치 이상인 frame 찾기
    arr_size = len(total_score)
    for i in range(0,arr_size):
        if(max_highlight_score <= total_score[i]):
            highlight_position.append(i)
    highlight_position.append(99999999)

    if(len(highlight_position)<2):
        print("No highlight")
        return 0
    #앞뒤 몇초
    index_size = 2
    start_index = 0
    final_index = 0
    index = 0
    index_result = 0
    while(index<len(highlight_position)-1):
        start_index = highlight_position[index]
        final_index = start_index
        for j in range(index,len(highlight_position)-1):
            if(highlight_position[j+1]-highlight_position[j]>index_size):
                final_index = highlight_position[j]
                index = j
                break
        index += 1
        #이번 하이라이트 씬이 한개일 경우 앞뒤 2초
        index_result += 1
        highlight.append(VideoFileClip(video).subclip(start_index-index_size,final_index+index_size))

    output = concatenate_videoclips([Start,highlight[0]],method="compose")
    for i in range(1,index_result):
        output = concatenate_videoclips([output,Sin,highlight[i]],method="compose")
    output = concatenate_videoclips([output,Finish],method="compose")   
    if os.path.exists("/outputVideo/output.mp4"):  
        shutil.rmtree("./__pycache__")
    output.write_videofile("./outputVideo/output.mp4")