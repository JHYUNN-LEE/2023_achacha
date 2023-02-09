from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests
import boto3
import os
import time
import pickle

#---------- input 값 -----------
category_list = ['가방', '귀금속', '도서용품', '서류', '쇼핑백', '스포츠용품', '유가증권',
                 '의류', '자동차', '전자기기', '지갑', '증명서', '컴퓨터', '카드', '현금', '휴대폰']
# category_list = ['컴퓨터']
region_list = ['서울', '경기도']

# input category dict
category_dict = {
    '가방' : 'PRA000', # 1
    '귀금속' : 'PRO000', # 2
    '도서용품' : 'PRB000', # 3
    '서류' : 'PRC000' , # 4
    '쇼핑백' : 'PRQ000', # 5
    '스포츠용품' : 'PRE000', # 6
    '유가증권' : 'PRM000', # 7
    '의류' : 'PRK000' , # 8
    '자동차' : "PRF000", # 9
    '전자기기' : 'PRG000' , # 10
    '지갑' : 'PRH000', # 11
    '증명서' : 'PRN000', # 12
    '컴퓨터' : 'PRI000', # 13
    '카드' : 'PRP000', # 14
    '현금' : 'PRL000', # 15
    '휴대폰' : 'PRJ000' # 16
}

# input save_name dict
category_en_dict = {
    '가방' : 'bag', # 1
    '귀금속' : 'jewelry', # 2
    '도서용품' : 'book', # 3
    '서류' : 'document' , # 4
    '쇼핑백' : 'shopping', # 5
    '스포츠용품' : 'sports', # 6
    '유가증권' : 'marketable', # 7
    '의류' : 'cloth' , # 8
    '자동차' : "car", # 9
    '전자기기' : 'electronic' , # 10
    '지갑' : 'wallet', # 11
    '증명서' : 'id', # 12
    '컴퓨터' : 'computer', # 13
    '카드' : 'card', # 14
    '현금' : 'cash', # 15
    '휴대폰' : 'phone' # 16
}

# input region
region_dict = {'서울' : 'LCA000', '경기도' : 'LCI000'}
region_en_dict = {'서울' : 'Seoul', '경기도' : 'Gyeonggi'}


#---------- Function -----------
# 마지막 페이지 넘버 찾기
def last_page(category, region, start_date, end_date):
    list_url = 'https://www.lost112.go.kr/find/findList.do'
    session = requests.Session()
    # session.headers.update(headers)
    resp = session.post(list_url, data={
        'PRDT_CL_CD01': category,
        'PRDT_CL_CD02': '',
        'START_YMD': start_date,
        'END_YMD': end_date,
        'PRDT_NM': '',
        'DEP_PLACE': '',
        'SITE': '',
        'PLACE_SE_CD': '',
        'FD_LCT_CD': region,
        'IN_NM': '',
        'ATC_ID': '',
        'MDCD': '',
        'SRNO': '',
        'IMEI_NO': '',
        'F_ATC_ID': '',
        'pageIndex': 1,
        'MENU_NO': ''
    }, timeout=100)

    # payload 대로 데이터 불러오기
    soup = bs(resp.text, 'html.parser')

    # 만약 맨 마지막 페이지로 가는 버튼이 있다면 맨 마지막 페이지의 태그의 값을 가져와준다.
    if soup.find("a", class_ = "last") :
        last = soup.find("a", class_ = "last")
        last_split =  last['onclick'].split("(")
        last_split_2 = last_split[1].split(")")
        last_num = last_split_2[0]

    # 마지막 페이지로 가는 버튼이 없으면 그냥 페이지네이션이 10페이지 내에 머물러 있기 때문에 a태그 맨 마지막 가져옴
    else:
        page_list = soup.find("div", class_ = "paging")
        last_num = page_list.find_all('a')[-1].get_text()

    return int(last_num)

def manage_list(category, pageidx, region, start_date, end_date):
    list_url = 'https://www.lost112.go.kr/find/findList.do'
    # Session 
    session = requests.Session()
    # session.headers.update({'User-Agent': 'Mozilla/5.0'})
    resp = session.post(list_url, data={
        'PRDT_CL_CD01': category,
        'START_YMD': start_date,
        'END_YMD': end_date,
        'PRDT_NM': '',
        'DEP_PLACE': '',
        'SITE': '',
        'PLACE_SE_CD': '',
        'FD_LCT_CD': region,
        'IN_NM': '',
        'ATC_ID': '',
        'MDCD': '',
        'SRNO': '',
        'IMEI_NO': '',
        'F_ATC_ID': '',
        'pageIndex': pageidx,
        'MENU_NO': ''

    }, timeout=100)

    # payload 대로 데이터 불러오기
    soup = bs(resp.text, 'html.parser')
    table = soup.find("table")

    # 관리번호 풀네임으로 가져오기
    tr_tags = table.find_all("tr")

    manage_num = []
    for i in range(1, len(tr_tags)):
        a_tag = tr_tags[i].find("a")
        a_tag_list = a_tag['href'].split("'")

        manage_num.append(a_tag_list[1] + '-' + a_tag_list[3] + '\n')

    return manage_num

            
def listDo():
    end = datetime.today()
    start = end + timedelta(days=-14)

    end_date = end.strftime("%Y%m%d")
    start_date = start.strftime("%Y%m%d")

    # 잦은 요청으로 오류나는 경우를 대비하여 sleep 걸어둠
    manageList = []
    for region in region_list:
        for category in category_list:
            try:
                lastPageNum = last_page(category_dict[category], region_dict[region], start_date, end_date)
            except:
                time.sleep(2)
                lastPageNum = last_page(category_dict[category], region_dict[region], start_date, end_date)

            for pageidx in range(1, lastPageNum+1):
                try:
                    manageList.extend(manage_list(category_dict[category], pageidx, region_dict[region], start_date, end_date))
                except:
                    time.sleep(2)
                    manageList.extend(manage_list(category_dict[category], pageidx, region_dict[region], start_date, end_date))
    
    ## datetime.datetime.now() 시 datetime이라는 변수가 없다는 오류 발생
    # nowdate = datetime.datetime.now()
    nowdate = datetime.now()
    filename = nowdate.strftime('%Y%m%d') + '_manageList'
        
    with open(f'{filename}.txt','a', encoding='UTF-8') as file:
        file.writelines(manageList)
        
    
    s3 = boto3.client('s3')
    

    try:
        s3.upload_file(f'{filename}.txt', "achachanew", f'manageList/{filename}.txt')
    except Exception as err:
        print("input error", err)


    file_path = f'/usr/local/airflow/dags/{filename}.txt'

    if os.path.exists(file_path):
        os.remove(file_path)
