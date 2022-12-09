import shutil
from turtle import width
from moviepy.editor import *

def frame_merge(video,total_score,start,sin,finish):
    #하이라이트 갯수
    max_highlight=3
    max_highlight_score = 8
    highlight = []
    highlight_position = []
    #앞뒤 몇초
    index_size = 3
    Start = VideoFileClip(start).subclip(0,1)
    Sin=VideoFileClip(sin)
    Sin=Sin.crossfadeout(1) #fadein 1초
    Finish=VideoFileClip(finish).subclip(0,1)
    
    for q in range(index_size):
        total_score[q] = 0
    
    ##현제 1초에 3frame
    # index_total = 0
    # new_index = 0
    # new_hightlight = []
    
    # print(1)
    # print(total_score)
    # while (index_total + 3 < arr_size):
    #     temp = total_score[index_total] + total_score[index_total + 1] + total_score[index_total + 2]
    #     new_hightlight.append(temp)
    #     index_total+=3

    # print(2)
    # print(new_hightlight)
    ##현제 1초에 3frame 여기까지


    #하이라이트 스코어가 일정 수치 이상인 frame 찾기
    arr_size = len(total_score)
    for i in range(0,arr_size):
        if(max_highlight_score <= total_score[i]):
            highlight_position.append(i)
    for q in range(index_size):
        highlight_position.append(99999999)


    if(len(highlight_position)<2):
        print("No highlight")
        return 0

    start_index = 0
    final_index = 0
    index = 0
    index_result = 0
    print("score chaine")
    print(highlight_position)
    while(index<len(highlight_position)-index_size):
        start_index = highlight_position[index]
        final_index = start_index
        for j in range(index,len(highlight_position)-1):
            if(highlight_position[j+1]-highlight_position[j]>index_size*2):
                final_index = highlight_position[j]
                index = j
                break
        index += 1
        #이번 하이라이트 씬이 한개일 경우 앞뒤 2초
        index_result += 1
        print(start_index-index_size,final_index+index_size)
        temp_clip = VideoFileClip(video).subclip(start_index-index_size,final_index+index_size)
        temp_clip = temp_clip.fadein(1.0)
        highlight.append(temp_clip)

    output = concatenate_videoclips([highlight[0]],method="chain")
    #output = concatenate_videoclips([Start,highlight[0]],method="compose")
    for i in range(1,index_result):
        output = concatenate_videoclips([output,highlight[i]],method="chain")

        #output = concatenate_videoclips([output,Sin,highlight[i]],method="compose")
    #output = concatenate_videoclips([output,Finish],method="compose")   
    if os.path.exists("/outputVideo/output.mp4"):  
        shutil.rmtree("./__pycache__")
    output.write_videofile("./outputVideo/output.mp4")

if __name__ == "__main__":
    start_dir = "./CutSin/Start.mp4"
    cut_dir = "./CutSin/Sin.mp4"
    finish_dir = "./CutSin/Finish.mp4"
    temp_score = [0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 10, 1, 1, 0, 1, 0, 0, 16.8804, 27.5269, 25.5269, 25.5269, 25.5269, 25.5269, 25.5269, 25.5269, 25.5269, 25.5269, 25.5269, 25.5269, 25.5269, 25.5269, 25.5269, 25.5269, 25.5269, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 8.9801, 4.641300000000001, 2.641300000000001, 2.641300000000001, 2.641300000000001, 2.641300000000001, 2.641300000000001, 2.641300000000001, 2.641300000000001, 2.641300000000001, 2.641300000000001, 2.641300000000001, 2.641300000000001, 2.641300000000001, 2.641300000000001, 2.641300000000001, 0.9801000000000004, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4.941099999999994, 4.941099999999994, 4.941099999999994, 4.941099999999994, 4.941099999999994, 4.941099999999994, 4.941099999999994, 4.941099999999994, 4.941099999999994, 4.941099999999994, 4.941099999999994, 4.941099999999994, 4.941099999999994, 4.941099999999994, 4.941099999999994, 4.941099999999994, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 6.321800000000004, 8.445400000000005, 5.445400000000005, 5.445400000000005, 5.445400000000005, 5.445400000000005, 5.445400000000005, 5.445400000000005, 5.445400000000005, 5.445400000000005, 5.445400000000005, 5.445400000000005, 5.445400000000005, 5.445400000000005, 5.445400000000005, 5.445400000000005, 0, 0, 0, 0, 999, 999, 999, 999, 999, 1003.1189, 1003.1189, 1004.7573, 1004.7573, 1004.7573, 1004.7573, 5.757299999999996, 5.757299999999996, 5.757299999999996, 5.757299999999996, 5.757299999999996, 5.757299999999996, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    frame_merge("./VideoFile/test2.mp4",temp_score,start_dir,cut_dir,finish_dir)