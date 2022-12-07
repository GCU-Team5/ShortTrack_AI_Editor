from objectDetection import Object_detection
import ocr
import STT_detection


def highlight(count,videopath):
    #count는 frame_divide에서 프레임 수

    #하이라이트 스코어 1.OCR 2.STT 3.진폭 4.Odject Detection 5.total score
    score_list = [[0 for j in range(count)] for i in range(4)]
    score_list[0] =  ocr.ocr_recognition()
    score_list[1] =STT_detection.STT_detection(count,videopath)
    temp_list  =  Object_detection()
    index_total = 0
    new_hightlight = []
    while (index_total + 3 < len(temp_list)):
        temp = temp_list[index_total] + temp_list[index_total + 1] + temp_list[index_total + 2]
        new_hightlight.append(temp)
        index_total+=3

    score_list[3] = new_hightlight


    #여기서 각 수치 종합 후 

    total_score=[0 for j in range(count)]
    #score 종합
    for i in range(0,count): 
        total_score[i]=score_list[0][i]+score_list[1][i]+score_list[2][i]+score_list[3][i]
    return total_score

if __name__ == "__main__":
    highlight(73,"./VideoFile/test2.mp4")