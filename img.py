from dotenv import load_dotenv
import os
from openai import AzureOpenAI
import base64
from mimetypes import guess_type

# Function to encode a local image into data URL 
def local_image_to_data_url(image_path):
    # Guess the MIME type of the image based on the file extension
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # Default MIME type if none is found
    
    # Read and encode the image file
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Construct the data URL
    return f"data:{mime_type};base64,{base64_encoded_data}"

def Extract_Info(image_path):
    load_dotenv()

    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT") # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
    api_key= os.getenv("AZURE_OPENAI_API_KEY")
    deployment_name = 'gpt-4o'

    client = AzureOpenAI(
        api_key= api_key, # 키 호출
        api_version= '2024-05-01-preview', # api 버전 호출
        base_url=f"{azure_endpoint}openai/deployments/{deployment_name}"
    )
    # Example usage
    data_url = local_image_to_data_url(image_path)

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            { "role": "system", "content": "You are a helpful assistant." },
            { "role": "user", "content": [  
                { 
                    "type": "text", 
                    "text": "Please extract and output the following information from the business card image encoded by base64 :\
                          list[이름, 회사이름, 직급, 부서, 직무, 주소, 전화번호, 이메일] in Korean. \
                            ex.) 홍길동, 삼성, CTO, LSI, 연구원, 서울특별시, 010-111-222, 123@naver.com (괄호없이 한 줄 나열)\
                                없는 항목은 None으로 출력해줘\
                                    예를 들어 직급은 과장, 부장, CTO등을 말하고, 직무는 연구원, 공인중개사 처럼 특정 직업 또는 하는 일을 나타내는 단어야. 잘 구분해주면 좋겠어."
                },
                { 
                    "type": "image_url",
                    "image_url": {
                        "url": data_url
                    }
                }
            ] } 
        ],
        max_tokens=2000 
    )

    text_content = response.choices[0].message.content
    info_list = text_content.split(', ')
    info_dic = {"name" : info_list[0], # 이름
                "company" : info_list[1], # 회사이름
                "position" : info_list[2], # 직급
                "department" : info_list[3], # 사업부
                "job_title" : info_list[4], # 직무
                "address" : info_list[5], # 회사주소
                "phone" : info_list[6], # 폰번호
                "email" : info_list[7], # 이메일
                }
    return info_dic

