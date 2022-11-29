import torch
import glob
import os
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

target=0 #fall_down의 index
threshhold=0.7 #객체인식 임계 확률

# model = torch.hub.load("C:/Users/KIM YAECHAN/Desktop/졸업작품/content/yolov5", 'custom', path="C:/Users/KIM YAECHAN/Desktop/졸업작품/content/yolov5/runs/train/skate3/weights/best.pt", source='local')

# img = 'C:/Users/KIM YAECHAN/Desktop/졸업작품/val/AnyConv.com__8.jpg'
# test='C:/Users/KIM YAECHAN/Documents/GitHub/ShortTrack-AIEditor/ShortTrack/images/temp/frame0.png'
# video='C:/Users/KIM YAECHAN/Desktop/졸업작품/test_video.mp4'



def Object_detection(target='fall_down',threshhold=0.5):
    
    target_id_to_name = ['fall_down','skating','start', 'finish']
    target_name_to_id = {target_id_to_name[i]: i for i in range(len(target_id_to_name))}
    
    #모델 파라미터 load
    model = torch.hub.load("yolov5", 'custom', path="./best.pt", source='local')
    
    #객체를 index번호로 바꿈
    target=target_name_to_id[target]
    score=[]

    #frame path
    images=sorted(glob.glob('./images/temp/*'), key=os.path.getctime)

    for fname in images:

        results=model(fname)

        # print(results.xyxyn)
        count_object=0 
        for result in results.xyxyn[0]:
            #인식한 개체가 target일때
            if result[-1]==target:
                #인식 confidence가 threshold보다 높은지 확인
                if result[-2]>=threshhold:
                    print('Detected')
                    count_object+=1

        score.append(count_object)
        #results.show()  
    print("objectDetectionScore:",score)
        
    return score


# print(Object_detection())