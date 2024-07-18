import streamlit as st
from PIL import Image
import pandas as pd
import os
import numpy as np

import database as db

# DB 초기화
columns = ['id', 'name', 'company', 'position', 'department', 'job_title', 'address', 'phone', 'email', 'photo']

# df = pd.DataFrame(data, columns=columns)

p_blob = db.ImageToBlob('/root/LLM_Bootcamp/image/images.jpeg')
db.AddDB("금쪽이현수","네이버","쫄따구","네이버 CLOVA","SW개발","경기 판교 정자","010-5294-2206","hyounshu@kookmin.ac.kr.",p_blob) # 사진 데이터 삽입할때 전처리필요.


# Function to display a business card list
def display_business_card_list(data, df):
    
    st.write("### 내 명함첩")
    st.write("---")
    for index, row in df.iterrows():
        cols = st.columns([4, 1])  # Adjust column width ratio as needed
        with cols[0]:
            st.write(f"**{row['name']}**")
            st.write(f"{row['position']} / {row['department']}")
            st.write(f"{row['company']}")
            if st.button(f"상세 정보 보기", key=index):
                st.session_state.page = 'details'
                st.session_state.selected_index = index
        with cols[1]:
            if row['photo'] is not None:
                
                iiiimage = db.BlobToImage(row['photo'])

                st.image(iiiimage, width=300)
            else:
                st.image("/root/LLM_Bootcamp/image/240_F_248426448_NVKLywWqArG2ADUxDq6QprtIzsF82dMF.jpg", width=200)  # Use a placeholder image
        st.divider()

# Function to display the details of a business card
def display_business_card_details(row):
    st.write("### 명함 상세 정보")
    st.write(f"**이름**: {row['name']}")
    st.write(f"**직책**: {row['position']}")
    st.write(f"**부서**: {row['department']}")
    st.write(f"**회사**: {row['company']}")
    # Display the image if available
    if row['photo'] is not None:
        iiiimage = db.BlobToImage(row['photo'])

        st.image(iiiimage, width=300)
    else:
        st.image("/root/LLM_Bootcamp/image/240_F_248426448_NVKLywWqArG2ADUxDq6QprtIzsF82dMF.jpg", width=300)  # Use a placeholder image

    if st.button("목록으로 돌아가기"):
        st.session_state.page = 'list'

# Function to display the upload page
def display_upload_page():
    st.write("### 명함 업로드")
    uploaded_image = st.file_uploader("명함 이미지를 업로드하세요", type=["png", "jpg", "jpeg"])

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption='Uploaded Business Card', use_column_width=True)
        # Here, you would typically call your business card recognition function
        # and append the new data to the DataFrame

    if st.button("목록으로 돌아가기"):
        st.session_state.page = 'list'
        st.experimental_rerun()


# Streamlit UI
st.title("카드매니저")

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = 'list'
if 'selected_index' not in st.session_state:
    st.session_state.selected_index = None
    
# Navigation buttons
if st.session_state.page != 'upload':
    cols = st.columns([1, 1, 1, 1])  # Adjust column width ratio as needed
    with cols[3]:
        if st.button("명함 업로드"):
            st.session_state.page = 'upload'
            st.experimental_rerun()

# Page navigation
if st.session_state.page == 'list':
    # st.write("### 등록된 명함")
    data = db.GetDB()
    df = pd.DataFrame(data, columns=columns)
    display_business_card_list(data, df)
elif st.session_state.page == 'details' and st.session_state.selected_index is not None:
    data = db.GetDB()
    df = pd.DataFrame(data, columns=columns)
    display_business_card_details(df.iloc[st.session_state.selected_index])
elif st.session_state.page == 'upload':
    display_upload_page()