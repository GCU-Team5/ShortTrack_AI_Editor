from PIL import Image
import base64
from io import BytesIO
import mysql.connector

def convertToBinaryData(filePath):
    # Convert digital data to binary format
    encoded = base64.b64encode(open(filePath, 'rb').read())
    return encoded

def insertHighlightTime(highlight_database):
    try:
        connection = mysql.connector.connect(
            host='database-1.cf3zdshpxfhs.ap-northeast-2.rds.amazonaws.com',
            database='ShortTrack',
            user='admin',
            password='demo0000'
        )
        cursor = connection.cursor()

        for highlight_database_data in highlight_database:
            sql_query = '''INSERT INTO ShortTrack.ST_HIGHLIGHT_INFO (HIGHLIGHT_TIME) VALUES (%s)'''
        
            result = cursor.execute(sql_query, (highlight_database_data,))
            connection.commit()
    except:
        print("Failed inserting BLOB data into MySQL table")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def insertBLOB(imagePath):
    try:
        connection = mysql.connector.connect(
            host='database-1.cf3zdshpxfhs.ap-northeast-2.rds.amazonaws.com',
            database='ShortTrack',
            user='admin',
            password='demo0000'
        )
        cursor = connection.cursor()

        img_blob = convertToBinaryData(imagePath)
        sql_query = '''INSERT INTO ShortTrack.ST_FRAME (IMAGE) VALUES (%s)'''
        # print(img_blob)
        img = Image.open(BytesIO(base64.b64decode(img_blob)))
        # img.show(img)
        print('connect success')

        result = cursor.execute(sql_query, (img_blob,))
        connection.commit()


    except:
        print("Failed inserting BLOB data into MySQL table")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def selectBLOB():
    try:
        connection = mysql.connector.connect(
            host='database-1.cf3zdshpxfhs.ap-northeast-2.rds.amazonaws.com',
            database='ShortTrack',
            user='admin',
            password='demo0000'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT IMAGE FROM ShortTrack.ST_FRAME")
        return cursor.fetchall()
    except:
        print("Failed selecting BLOB data into MySQL table")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def insertSTVideoTable(video_name, game_type, broadcast_date):
    try:
        connection = mysql.connector.connect(
            host='database-1.cf3zdshpxfhs.ap-northeast-2.rds.amazonaws.com',
            database='ShortTrack',
            user='admin',
            password='demo0000'
        )
        cursor = connection.cursor()
        sql_query = '''INSERT INTO ShortTrack.ST_VIDEO (VIDEO_NAME, GAME_TYPE, BROADCAST_DATE)
VALUES(%s, %s, %s)'''
        insertTuple = (video_name, game_type, broadcast_date)
        result = cursor.execute(sql_query, insertTuple)
        connection.commit()

    except:
        print("Failed inserting data into MySQL table")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def database_send(highlight_database):
    #하이라이트 타임을 넣는 것
    insertHighlightTime(highlight_database)

def selectST_HIGHLIGHT_INFO():
    try:
        connection = mysql.connector.connect(
            host='database-1.cf3zdshpxfhs.ap-northeast-2.rds.amazonaws.com',
            database='ShortTrack',
            user='admin',
            password='demo0000'
        )
        cursor = connection.cursor()
        sql_query = "SELECT HIGHLIGHT_TIME FROM ShortTrack.ST_HIGHLIGHT_INFO"
        cursor.execute(sql_query)

        results = cursor.fetchall()
        return results

    except:
        print("Failed inserting data into MySQL table")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


# insertBLOB('./images/frame0.png')

#이미지 디비에서 꺼낸다음 base64 디코딩
# res = selectBLOB()
# print('finish')
# print(type(str(res[9]))) #frame1
# tempStr = str(res[9])
# print(tempStr[3:-3])
# lastStr = tempStr[3:-3]
# str_new = lastStr + '='*(4-len(lastStr)%4)
# img = Image.open(BytesIO(base64.b64decode(str_new)))
# img.show(img)
# insertSTVideoTable('세계선수권', '월드컵', '2019-11-04')
