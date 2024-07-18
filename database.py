import sqlite3
import os
from PIL import Image
import io
# SQLite 데이터베이스 파일 경로
PATH_NAME = "ttt.db"
ID = 0
NAME = 1
COMPANY = 2
POSITION = 3
DEPARTMENT = 4
JOB_TITLE = 5
ADDRESS = 6
PHONE= 7
EMAIL = 8
PHOTO = 9

# 데이터 베이스에 정보 추가하는 함수.
def AddDB(name,company,position,department,job_title,address,phone,email,photo,path_name = PATH_NAME) :
    # 데이터 베이스와 연결
    conn = sqlite3.connect(path_name)
    
    try :
        # 커서 생성
        cursor = conn.cursor()
        
        # user_info 테이블 생성
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT, 
                    company TEXT,
                    position TEXT,
                    department TEXT,
                    job_title TEXT,
                    address TEXT,
                    phone TEXT,
                    email TEXT,
                    photo BLOB
                )''')
        
        # 데이터 삽입.
        cursor.execute('''INSERT INTO user_info (name, company, position, department, job_title, address, phone, email, photo)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (name, company, position, department, job_title, address, phone, email, photo))
        
        # 커밋 (데이터베이스에 변경사항 반영)
        conn.commit()
        
        print("데이터 추가 성공!")
    
    finally :
        conn.close()

# 데이터 베이스 모든 내용 출력하는 함수
def PrintDB(db_path = PATH_NAME, table_name = "user_info") :
    # 데이터 베이스와 연결
    conn = sqlite3.connect(db_path)
    # 커서 생성
    cursor = conn.cursor()
    # 데이터 불러오기
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    # 데이터 출력
    # for row in rows:
    #     print(row)
    for row in rows:
        for index,data in enumerate(row) :
            if index == PHOTO :
                print("good!",end = " ")
                continue
            print(data,end=' ')
        print("")
            
    # 연결 종료
    conn.close()

# 데이터 베이스 모든 데이터 얻어내는 함수 format -> [(?),()] list + tuple
def GetDB(db_path = PATH_NAME, table_name = "user_info") :
    # 데이터 베이스와 연결
    conn = sqlite3.connect(db_path)
    
    # 커서 생성
    cursor = conn.cursor()
    
    # 데이터 불러오기
    cursor.execute(f"SELECT * FROM {table_name}")
    all_db_data = cursor.fetchall()
    
    # 연결 종료
    conn.close()
    return all_db_data

# DB 특정 행 삭제 가능. ex) DelDB(7) 7번 행을 지움.
def DelDB(record_id, db_path= PATH_NAME, table_name="user_info"):
    # 데이터 베이스와 연결
    conn = sqlite3.connect(db_path)
    
    # 커서 생성
    cursor = conn.cursor()
    
    # 데이터 삭제
    cursor.execute(f"DELETE FROM {table_name} WHERE id=?", (record_id,))
    
    # 커밋 (데이터베이스에 변경사항 반영)
    conn.commit()
    
    print(f"ID {record_id} 데이터 삭제 완료!")
    
    # 연결 종료
    conn.close()

# 사진 데이터 Blob 데이터로 바꿔주는 함수
def ImageToBlob(file_path):
    with open(file_path, 'rb') as f:
        photo_blob = f.read()
    return photo_blob

def BlobToImage(blob_data) :
    try:
        # BLOB 데이터를 이미지로 변환
        image = Image.open(io.BytesIO(blob_data))
        
        # 이미지를 원하는 파일 포맷으로 저장 (파일 확장자에 따라 자동으로 포맷 설정)
        return image
    
    except Exception as e:
        print(f"이미지 변환 중 오류 발생: {e}")
    

# DB의 테이블 하나를 전부 지워버리는 함수
def ClearDB_Table(table_name = 'user_info', db_path=PATH_NAME):
    # 데이터베이스와 연결
    conn = sqlite3.connect(db_path)
    # 커서 생성
    cursor = conn.cursor()
    
    # 테이블의 모든 데이터 삭제 (TRUNCATE)
    cursor.execute(f"DELETE FROM {table_name}")
    
    # 커밋 (데이터베이스에 변경사항 반영)
    conn.commit()
    
    print(f"{table_name} 테이블의 모든 데이터 삭제 완료!")
    
    # 연결 종료
    conn.close()

# DB 자체를 지워버리는 함수.
def RemoveDB(db_path):
    try:
        # 데이터베이스 파일 삭제
        os.remove(db_path)
        print(f"데이터베이스 {db_path} 삭제 완료!")
    except FileNotFoundError:
        print(f"데이터베이스 {db_path}가 이미 존재하지 않습니다.")
    except Exception as e:
        print(f"데이터베이스 삭제 중 오류 발생: {e}")



# p_blob = ImageToBlob('/root/LLM_Bootcamp/LangChain_class/Model_IO/스크린샷 2024-05-14 233747.png')
# BlobToImage(p_blob)

# AddDB("금쪽이현수","네이버","쫄따구","네이버 CLOVA","SW개발","경기 판교 정자","010-5294-2206","hyounshu@kookmin.ac.kr.",p_blob) # 사진 데이터 삽입할때 전처리필요.
# PrintDB()
# ClearDB_Table()
# PrintDB()
# RemoveDB("ttt.db")
        
    