from objectDetection import Object_detection
import ocr
import STT_detection
import pandas as pd
# from xgboost import XGBClassifier


def highlight(count,videopath):
    #count는 frame_divide에서 프레임 수

    

    #하이라이트 스코어 1.OCR 2.STT 3.진폭 4.Odject Detection 5.total score
    score_list = [[0 for j in range(count)] for i in range(4)]
    score_list[0],xg_OCR =  ocr.ocr_recognition(count)
    score_list[1],xg_STT =STT_detection.STT_detection(count,videopath)
    temp_list,xgb_OB =  Object_detection(count)
    index_total = 0
    new_hightlight = []
    while (index_total + 3 < len(temp_list)):
        temp = temp_list[index_total] + temp_list[index_total + 1] + temp_list[index_total + 2]
        new_hightlight.append(temp)
        index_total+=3
        
    new_hightlight.append(0)

    score_list[3] = new_hightlight


    #여기서 각 수치 종합 후 

    total_score=[0 for j in range(count)]
    #score 종합

    print('Count',count)
    print(len(total_score))
    print(len(score_list[0]))
    print(len(score_list[1]))
    print(len(score_list[2]))
    print(len(score_list[3]))


    for i in range(0,count): 

        print(i)
        total_score[i]=score_list[0][i]+score_list[1][i]+score_list[2][i]+score_list[3][i]



    index_OB_xgb = 0
    xg_Object_F= []
    xg_Object_SF= []
    xg_STT1=[]
    xg_STT2=[]
    while(index_OB_xgb +3<len(xgb_OB)):
        if(xgb_OB[index_OB_xgb][0]==1 | xgb_OB[index_OB_xgb+1][0]==1 | xgb_OB[index_OB_xgb+2][0]==1):
            xg_Object_F.append(1)
        else:
            xg_Object_F.append(0)
        if(xgb_OB[index_OB_xgb][1]==1 | xgb_OB[index_OB_xgb+1][1]==1 | xgb_OB[index_OB_xgb+2][1]==1):
            xg_Object_SF.append(1)
        else:
            xg_Object_SF.append(0)
        
        index_OB_xgb +=3

    for i in range(0,count):
        xg_STT1.append(xg_STT[i][0])
        xg_STT2.append(xg_STT[i][1])
    df = pd.DataFrame((zip(xg_Object_F,xg_Object_SF,xg_OCR,xg_STT1,xg_STT2)), columns = ['fall_down','start_finsh','rank_change', 'keyword', 'frequency'])


    print('df',df)
    df.to_csv("train_xgb.csv", mode='w')

    # xgBoost 모델 불러오기
    # xgb_model = XGBClassifier() # 모델 초기화
    # xgb_model.load_model('./xgboost.model')

    # y_pred = xgb_model.predict(df)
    # y_pred

    return total_score

if __name__ == "__main__":
    highlight(73,"./VideoFile/test2.mp4")