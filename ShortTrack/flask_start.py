import database
import frame_divide
import frame_merge
import highlight


def flask_start(video_path):
    #cutsin 변수
    start_dir = "./CutSin/Start.mp4"
    cut_dir = "./CutSin/Sin.mp4"
    finish_dir = "./CutSin/Finish.mp4"

    #fame_divide로 동영상 파일 넘긴뒤 실행
    count,imagePath = frame_divide.frame_divide(video_path)
    print("Finish divide")
    #하이라이트 실행
    total_score=highlight.highlight(count,video_path)
    print("\nTotal score",total_score)
    #merge실행
    highlight_database = frame_merge.frame_merge(video_path,total_score,start_dir,cut_dir,finish_dir)
    #database 연동
    database.database_send(highlight_database)
    database_file= database.selectST_HIGHLIGHT_INFO()

    # 텍스트 파일 생성 및 작성
    file_path = './outputVideo/highlight_time.txt'  # 생성할 파일의 경로와 이름 지정

    with open(file_path, 'w') as file:
        file.write('Highlight second information.\n\n')
        file.write(str(database_file))
    print('텍스트 파일이 생성되었습니다.')
    print("Finish")

