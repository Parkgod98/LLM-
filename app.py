import streamlit as st
from PIL import Image
import pandas as pd
import os

import database as db
import img as info

db.RemoveDB('tttt.db')

PLACEHOLDER_IMG_PATH = "placeholer_img.jpg"

# DB 초기화
columns = ['id', 'name', 'company', 'position', 'department', 'job_title', 'address', 'phone', 'email', 'photo']

# Function to display a business card list
def display_business_card_list(data, df):
    st.write("### 내 명함첩")
    st.write("---")
    for index, row in df.iterrows():
        cols = st.columns([4, 1])  
        with cols[0]:
            st.write(f"**{row['name']}**")
            st.write(f"{row['company']}")
            st.write(f"{row['department']} / {row['position']}")
            if st.button(f"상세 정보 보기", key=index):
                st.session_state.page = 'details'
                st.session_state.selected_index = index
                st.rerun()
        with cols[1]:
            if row['photo'] is not None:
                
                iiiimage = db.BlobToImage(row['photo'])

                st.image(iiiimage, width=300)
            else:
                st.image(PLACEHOLDER_IMG_PATH, width=200)  
        st.divider()


# Function to display the details of a business card
def display_business_card_details(row):
    st.write("### 명함 상세 정보")
    st.write(f"**이름**: {row['name']}")
    st.write(f"**회사**: {row['company']}")
    st.write(f"**부서**: {row['department']}")
    st.write(f"**직급**: {row['position']}")
    st.write(f"**직무**: {row['job_title']}")
    st.write(f"**주소**: {row['address']}")
    st.write(f"**전화번호**: {row['phone']}")
    st.write(f"**이메일**: {row['email']}")
    # Display the image if available
    if row['photo'] is not None:
        iiiimage = db.BlobToImage(row['photo'])

        st.image(iiiimage, width=300)
    else:
        st.image(PLACEHOLDER_IMG_PATH, width=300)  # Use a placeholder image

    if st.button("목록으로 돌아가기"):
        st.session_state.page = 'list'
        st.rerun()

# Function to display the upload page
def display_upload_page():
    st.write("### 명함 업로드")
    uploaded_image = st.file_uploader("명함 이미지를 업로드하세요", type=["png", "jpg", "jpeg"])

    if uploaded_image:
        card_image = Image.open(uploaded_image)
        
        save_path = 'upload_card_image.jpg'
        card_image.save(save_path)
        forward_path = os.path.abspath(save_path)
        
        info_dict = info.Extract_Info(forward_path)
        
        p_blob = db.ImageToBlob(forward_path)
        
        db.AddDB(info_dict['name'], info_dict['company'], info_dict['position'], 
                 info_dict['department'], info_dict['job_title'], info_dict['address'], 
                 info_dict['phone'], info_dict['email'], p_blob)
        
        st.image(card_image, caption='업로드 완료!', use_column_width=True)
        
        st.session_state.page = 'list'
        st.rerun()

    if st.button("목록으로 돌아가기"):
        st.session_state.page = 'list'
        st.rerun()


# Streamlit UI

st.title("카드 매니저")

if 'page' not in st.session_state:
    # db.AddDB("홍길동","네이버","사원","네이버 CLOVA","SW개발","경기 판교 정자","010-0000-0000","example@naver.com",db.ImageToBlob(PLACEHOLDER_IMG_PATH))
    st.session_state.page = 'list'
if 'selected_index' not in st.session_state:
    st.session_state.selected_index = None
    
# Navigation buttons
if st.session_state.page != 'upload':
    cols = st.columns([1, 1, 1, 1]) 
    with cols[3]:
        if st.button("명함 업로드"):
            st.session_state.page = 'upload'
            st.rerun()


# Page navigation
if st.session_state.page == 'list':
    data = db.GetDB()
    df = pd.DataFrame(data, columns=columns)
    
    df = df.sort_index(ascending=False)
    
    display_business_card_list(data, df)
elif st.session_state.page == 'details' and st.session_state.selected_index is not None:
    data = db.GetDB()
    df = pd.DataFrame(data, columns=columns)
    display_business_card_details(df.iloc[st.session_state.selected_index])
elif st.session_state.page == 'upload':
    display_upload_page()
