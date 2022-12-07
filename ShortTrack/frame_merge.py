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
    
    #arr_size = len(total_score)
    
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
    total_score[0] = 0
    total_score[1] = 0
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
    print("score chaine")
    print(highlight_position)
    while(index<len(highlight_position)-1):
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
    temp_score =[2997, 2997, 2997, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 33.5598, 23.559800000000003, 23.559800000000003, 23.559800000000003, 23.559800000000003, 16.4309, 0, 0, 1, 1.5873999999999997, 11.587399999999999, 1.5873999999999997, 6.5874, 1.5873999999999997, 1.5873999999999997, 0, 0, 0, 3.224499999999999, 103.2245, 104.2245, 3.224499999999999, 4.224499999999999, 2.121999999999997, 0, 100, 100, 156, 5.4162, 53.416199999999996, 2.4161999999999995, 2.4161999999999995, 2.4161999999999995, 100, 150, 100, 100, 150, 150, 150, 50, 200, 100, 150, 0, 0, 1, 0, 0, 50, 50, 10, 50, 150, 250, 250, 300, 150, 150, 150, 150, 100, 150, 150, 150, 100, 100, 100, 0, 0, 0, 50, 150, 100, 250, 300, 300, 300, 250, 999, 150, 50, 0, 0, 0, 0, 0, 2997, 50, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 150, 0, 50, 0, 50, 50, 50, 100, 0, 50, 150, 150, 150, 150, 50, 50, 999, 50, 999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 10, 100, 100, 150, 100, 0, 0, 0, 0, 0, 50, 150, 150, 100, 50, 0, 50, 0, 1998, 1998, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 0, 100, 0, 1, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 999, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1998, 2997, 1998, 2997, 1998, 2997, 999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 999, 2997, 2997, 2997, 2997, 2997, 2997, 2997, 2997, 2997, 2997, 0, 0, 0, 0, 1, 1, 0, 1, 0, 31.480999999999998, 21.480999999999998, 21.480999999999998, 21.480999999999998, 21.480999999999998, 0, 0, 0, 0, 0.7801999999999996, 0.7801999999999996, 0.7801999999999996, 0.7801999999999996, 0.7801999999999996, 0, 0, 0, 0, 4.570900000000003, 2.5709000000000026, 2.5709000000000026, 2.5709000000000026, 2.5709000000000026, 0, 0, 0, 0, 4.272499999999999, 3.4406, 1.4405999999999997, 2.4406, 1000.4406, 1001.2725, 0, 0, 1998, 999, 1.0420999999999998, 1.0646, 4.0421, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2997, 2997, 1998, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1998, 0, 2998, 0, 0, 0, 50, 50, 50, 100, 50, 0, 0, 1, 100, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1998, 999, 0, 0, 1049, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 10, 0, 10, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 999, 0, 0, 0, 0, 0, 0, 0, 0, 1049, 2997, 2997, 2997, 2997, 2997, 999, 0, 0, 0, 0, 999, 0, 2997, 2997, 2997, 3007, 2997, 2997, 2997, 2997, 1998, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 2997, 2997, 1998, 1049, 50, 0, 0, 0, 0, 0, 0, 50, 999, 2997, 1998, 2998, 2997, 2997, 2997, 2997, 2997, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14.0, 28.9665, 23.9665, 23.9665, 23.9665, 23.9665, 0, 0, 0, 0, 1.3213000000000004, 1.3213000000000004, 1.3213000000000004, 1.3213000000000004, 1.3213000000000004, 0, 0, 0, 5, 9.235799999999998, 4.235799999999997, 14.235799999999998, 4.235799999999997, 4.235799999999997, 0, 0, 0, 2.209999999999999, 9.481399999999997, 3.4813999999999976, 4.481399999999997, 1003.4814, 1003.4814, 0, 0, 2998, 1, 5.418099999999999, 2.4180999999999995]
    frame_merge("./VideoFile/test2.mp4",temp_score,start_dir,cut_dir,finish_dir)
