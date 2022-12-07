import cv2 #OpenCV 라이브러리
import os   #파일 디렉토리 라이브러리
import shutil

def frame_divide(video):
    imagePath = './images/'
    try:
        #임시로 파일이 있으면 삭제하는거 만든거
        if os.path.exists(imagePath):
            shutil.rmtree(imagePath)
        if not (os.path.isdir(video)):
            os.makedirs(os.path.join(imagePath + "temp"))
            os.makedirs(os.path.join(imagePath + "temp2"))

            cap = cv2.VideoCapture(video)

            #이미지 수
            count = 0
            count2 = 0
            while True:
                ret, image = cap.read()
                # 이미지 사이즈 960x540으로 변경
                # image = cv2.resize(image, (960, 540))

                if not ret:
                    break
                
                if(int(cap.get(1)) % 10 == 0):#29이 1초
                    if(count%3==0):
                        cv2.imwrite(imagePath + "temp" + "/frame%d.png" % count2, image)
                        count2 += 1
                    cv2.imwrite(imagePath + "temp2" + "/frame%d.png" % count, image)

                    print('%d.png done' % count)
                    count += 1

            cap.release()
            imagePath = imagePath+"temp"
            cv2.destroyAllWindows()

    except OSError as e:
        if e.errno != e.EEXIST:
            print("Failed to create directory!!!!!")
            raise
    return count2,imagePath