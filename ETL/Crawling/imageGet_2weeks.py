from botocore.exceptions import NoCredentialsError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup as bs
import time
import requests
import mimetypes
import json
import boto3

# s3에서 관리번호 추출하는 함수
def manage_list():
    s3 = boto3.client('s3')
    nowdate = datetime.now()
    listFilename = nowdate.strftime('%Y%m%d') + '_detailDictList'

    response = s3.get_object(Bucket='achachanew', Key=f'detailDictList/{listFilename}.json')
    body = response['Body'].read().decode('utf-8')
    lines = body.split('\n')
    detailDictList= json.loads(body)

    # 관리번호 추출
    manageList = []
    for value in range(len(detailDictList)):
        manageList.append(detailDictList[value]['관리번호'])
    
    # manageNumList, manageSubnumList 생성
    manageNumList = []
    manageSubnumList = []
    for num in range(len(manageList)):
        manageNumList.append(manageList[num].split("-")[0])
        manageSubnumList.append(manageList[num].split("-")[1])

    return manageNumList, manageSubnumList
    
    
# 이미지를 S3에 저장하는 함수
def upload_image(manage_num, manage_subnum, start_date, end_date):
    detail_url = 'https://www.lost112.go.kr/find/findDetail.do'
    # Session 
    session = requests.Session()
    # session.headers.update(headers)
    resp = session.post(detail_url, data={
        'PRDT_CL_CD01': '',
        'PRDT_CL_CD02': '',
        'START_YMD': start_date,
        'END_YMD': end_date,
        'PRDT_NM': '',
        'DEP_PLACE': '',
        'SITE': '',
        'PLACE_SE_CD': '',
        'FD_LCT_CD': 'LCA000',
        'IN_NM': '',
        'MDCD': '',
        'SRNO': '',
        'IMEI_NO': '',
        'F_ATC_ID': '',
        'ATC_ID': manage_num,
        'FD_SN': manage_subnum,
        'MENU_NO': ''
    }, timeout=100)

    soup = bs(resp.text, 'html.parser')

    # imgurl 만들기
    div_detail = soup.find("div", class_="findDetail")

    
    # div 태그를 못찾는 경우
    try:
        img_list = div_detail.find("img")["src"]
        if not "no_img" in img_list:
            img = img_list
        remote_url = ("https://www.lost112.go.kr" + img)
        num = soup.find("p", class_="find02").text
        
        # 이미지를 S3에 저장
        s3 = boto3.client('s3')
        
        try:
            imageResponse = requests.get(remote_url, stream=True).raw
            content_type = imageResponse.headers['content-type']
            extension = mimetypes.guess_extension(content_type)
            bucket = 'achachanew'

            s3.upload_fileobj(imageResponse, bucket, f'images/{num}.jpg')

            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False
    except:
        pass
    
    
    

def imageGet():
    end = datetime.today()
    start = end - relativedelta(days=-14)
    
    end_date = end.strftime("%Y%m%d")
    start_date = start.strftime("%Y%m%d")

    manageNumList, manageSubnumList = manage_list()
    for manageNum, manageSubnum in zip(manageNumList, manageSubnumList):
        try:
            upload_image(manageNum, manageSubnum, start_date, end_date)
        # 잦은 요청으로 requests 오류가 날 시 sleep으로 버퍼를 줌
        except:
            time.sleep(2)
            upload_image(manageNum, manageSubnum, start_date, end_date)
