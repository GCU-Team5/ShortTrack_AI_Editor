#import pytesseract
import glob

import cv2
from google.cloud import vision
import io
import os
#구글 vision api 코드
#gram json 경로
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\googleCloudApiJson\shorttrack-ocr-f05377351806.json"

#MAC json 경로

def ocr_recognition():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_json\shorttrack2-637100724bf4.json"
    client = vision.ImageAnnotatorClient()
    #잘려진 frame 이미지 ocr 인식하기
    #set, dic, hash, list
    #keyword list -> keywords
    keywords = ['준준결승', '준결승', '결승',
                '500m', '1000m', '1500m', '3000m', '5000m', '계주',
                '남자', '여자',
                'final lap', 'lap:', 'speed',
                '곽윤기', '최민정',
                '대한민국', '한국']

    keywordsScore = [2, 4, 6,
                      3, 6, 9, 12, 15, 18,
                      4, 8,
                      5, 10, 15,
                      6, 12,
                      7, 14]


    #set 딕셔너리 중복없고 순서없다.
    #순위 리스트 생성
    imgKeywordSet = set()

    ranking = []
    scoreList = []
    firstPlace = ""
    secondPlace = ""
    thirdPlace = ""

    speed = ""
    images = sorted(glob.glob('./images/temp/*'), key=os.path.getctime)

    for path in images:
        try:

            with io.open(path, 'rb') as image_file:
                content = image_file.read()


            image = vision.Image(content=content)
            response = client.text_detection(image=image)
            texts = response.text_annotations
            content = texts[0].description
            content = content.replace(',','')
            # print(content)
            #content = content.lower() 소문자로 변환을 여기서 할지 밑에서 할지 고민

            #content str 형

            #객체 지향으로 만들기
            #1.  ~ \n
            #2.  ~ \n
            #3.  ~ \n

            lapTime = []  # dongmin
            splitWords = content.split('\n')
            # print("splitWords: ", splitWords)
            for splitWord in splitWords:
                if splitWord.startswith("1. "):
                    firstPlace = splitWord
                if splitWord.startswith("2. "):
                    secondPlace = splitWord
                if splitWord.startswith("3. "):
                    thirdPlace = splitWord
                if 'Lap:' in splitWord:  # dongmin change
                    temp = splitWord.split(':')  # dongmin
                    lapTime.append(temp[1])  # dongmin
                if 'Speed' in splitWord:
                    speed = splitWord

            # lap time socore under the 8.40time :10//// 8.5:8////8.7:6////8.
            lap_rank_socre = 0
            if (len(lapTime) != 0):
                for lap_speed_rank in range(3):
                    lap_rank_score_temp = 10
                    lap_rank_score_temp -= float(lapTime[lap_speed_rank])
                    lap_rank_socre += lap_rank_score_temp ** 3

            ranking.append(firstPlace)
            ranking.append(secondPlace)
            ranking.append(thirdPlace)
            #print("first place: {}, second place: {}, thrid place: {}".format(firstPlace, secondPlace, thirdPlace))


            #content를 모두 소문자로 변경 -> 키워드 찾기
            #print("content: \n", content)

            for keyword in keywords:
                if keyword in content:
                    #print(keyword, 'is in image')
                    imgKeywordSet.add(keyword)

            frameScore = lap_rank_socre
            scoreList.append(frameScore)


        # print("ranking: ", ranking)
        # print()
        #
        #
        # print()
        # print("img keyword Set: ", imgKeywordSet)
        # print()
        # print("lap time: ", lapTime)
        # print()




        except:
            print("ocr 결과가 없습니다.")
            scoreList.append(0)

    rankingScoreList = rankingChangeScore(ranking)
    # print("ranking score list: ", rankingScoreList)
    # print()
    # print("score lap list: ", scoreList)

    for i in range(len(rankingScoreList)):
        scoreList[i] += rankingScoreList[i]

    # print()
    print("Final Result: ", scoreList)
    return scoreList

    #준결승이 content에 있으면 준결승이라 정확히 인식하지만 결승도 인식을 해버리는 문제 발생

def rankingChangeScore(ranking):

    # ranking = ['1. LI J.', '2. CHOI M..', '3. QU C.',
    #            '1. LI J.', '2. CHOI M..', '3. QU C.',
    #            '1. L. GEHRING', '2. K. BOUTIN', '3. KIM A.L.',
    #            '1. L. GEHRING', '2. K. BOUTIN', '3. KIM A.L.',
    #            '1. K. BOUTIN', '2. L. van RUIJVEN', '3. KIM A.L.']


    scoreList = [0]
    rankingListLen = len(ranking)

    i = 0

    for j in range((rankingListLen // 3) - 1):
        # 1위 변동: 5점, 2위 변동: 3점, 3위 변동: 2점

        score = 0

        firstPlaceFront = ranking[i]
        secondPlaceFront = ranking[i + 1]
        thirdPlaceFront = ranking[i + 2]

        firstPlaceRear = ranking[i + 3]
        secondPlaceRear = ranking[i + 4]
        thirdPlaceRear = ranking[i + 5]
        i = i + 3

        if (firstPlaceFront != firstPlaceRear):
            score = score + 5
        if(secondPlaceFront != secondPlaceRear):
            score = score + 3
        if(thirdPlaceFront != thirdPlaceRear):
            score = score + 2

        scoreList.append(score)

    return scoreList








if __name__ == "__main__":
    ocr_recognition()
    #print(rankingChangeScore())
