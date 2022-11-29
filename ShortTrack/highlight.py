from objectDetection import Object_detection
import OCR
import STT_detection


def highlight(count):
    #count는 frame_divide에서 프레임 수

    #하이라이트 스코어 1.OCR 2.STT 3.진폭 4.Odject Detection 5.total score
    score_list = [[0 for j in range(count)] for i in range(4)]
    score_list[0] =  OCR.ocr_recognition()
    score_list[1] =  STT_detection.STT_detection(count)
    score_list[3] = Object_detection()


    #여기서 각 수치 종합 후 

    total_score=[0 for j in range(count)]
    #score 종합
    for i in range(0,count): 
        total_score[i]=score_list[0][i]+score_list[1][i]+score_list[2][i]+score_list[3][i]
    return total_score