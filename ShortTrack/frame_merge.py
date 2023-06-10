import shutil
from turtle import width
from moviepy.editor import *

def frame_merge(video,total_score,start,sin,finish):
    #하이라이트 갯수
    max_highlight=3
    max_highlight_score = 8
    highlight = []
    highlight_position = []
    highlight_database = []
    #앞뒤 몇초
    index_size = 3
    Start = VideoFileClip(start).subclip(0,1)
    Sin=VideoFileClip(sin)
    Sin=Sin.crossfadeout(1) #fadein 1초
    Finish=VideoFileClip(finish).subclip(0,1)
    
    for q in range(index_size+1):
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
        highlight_database.append(str(start_index-index_size)+"~"+str(final_index+index_size))
        temp_clip = VideoFileClip(video).subclip(start_index-index_size,final_index+index_size)
        temp_clip = temp_clip.fadein(1.0)
        highlight.append(temp_clip)

    print(highlight_database)

    output = concatenate_videoclips([highlight[0]],method="compose")
    #output = concatenate_videoclips([Start,highlight[0]],method="compose")
    for i in range(1,index_result):
        output = concatenate_videoclips([output,highlight[i]],method="compose")

        #output = concatenate_videoclips([output,Sin,highlight[i]],method="compose")
    #output = concatenate_videoclips([output,Finish],method="compose")   
    if os.path.exists("/outputVideo/output.mp4"):  
        shutil.rmtree("./__pycache__")
    output.write_videofile("./outputVideo/output.mp4")
    return(highlight_database)

if __name__ == "__main__":
    start_dir = "./CutSin/Start.mp4"
    cut_dir = "./CutSin/Sin.mp4"
    finish_dir = "./CutSin/Finish.mp4"
    temp_score = [49, 0, 0, 51, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 2997, 2997, 2997, 2997, 2997, 2997, 2997, 2997, 2998, 2998, 1, 0, 0, 0, 1, 1, 1, 51, 10, 11, 10, 11, 11, 10, 20, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 50, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 9, 9, 8, 8, 9, 8, 16, 0, 0, 0, 2, 5, 5, 5, 5, 8, 11, 9.1781, 4.178100000000001, 8.1781, 8.1024, 11, 5, 6, 5, 11, 1.3612999999999997, 0.642199999999999, 8.642199999999999, 8.642199999999999, 9, 9, 9, 9, 17, 4.336900000000001, 4.336900000000001, 13.3369, 1012.3369, 1159, 111, 160, 60, 3018, 1001.928, 3.1379999999999972, 0, 0, 0, 0]
    frame_merge("./VideoFile/final!!.mp4",temp_score,start_dir,cut_dir,finish_dir)