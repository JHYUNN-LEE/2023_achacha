# python packages
from datetime import datetime, timedelta
from hdfs import InsecureClient
import boto3
import json
import os

def yesterday_detailDo():
    s3 = boto3.client('s3')
    # 어제 날짜
    yesterday = datetime.now() - timedelta(1)
    filename = yesterday.strftime('%Y%m%d') + '_detailDictList'
    
    response = s3.get_object(Bucket='achachanew', Key=f'detailDictList/{filename}.json')
    body = response['Body'].read().decode('utf-8')
    yesterdayDictList = json.loads(body)

    return yesterdayDictList


def update():
    #---------- 오늘 값 -----------
    # Today detatilDo
    s3 = boto3.client('s3')
    nowdate = datetime.now()
    filename = nowdate.strftime('%Y%m%d') + '_detailDictList'
    response = s3.get_object(Bucket='achachanew', Key=f'detailDictList/{filename}.json')
    body = response['Body'].read().decode('utf-8')
    todayDetailList= json.loads(body)
    
    # Today manageList
    newManageList = []
    for value in range(len(todayDetailList)):
        newManageList.append(todayDetailList[value]['관리번호'])
        
    #---------- 어제 값 -----------
    # Yesterday detailDo
    yesterdayDictList = yesterday_detailDo()
    
    # Yesterday managelist
    orgManageList = []
    for value in range(len(yesterdayDictList)):
        orgManageList.append(yesterdayDictList[value]['관리번호'])

    
    # 어제와 오늘의 listdo 관리번호 비교하여 
    # 사이트에서 사라진 관리번로를 deleteManageNum에 추가해줌
    deleteManageList = []
    for value in orgManageList:
        if value not in newManageList: 
            deleteManageList.append(value)
    

    # 어제 + 오늘 detailDo를 updateDetailList에 저장해줌
    for i in range(len(yesterdayDictList)):
        if yesterdayDictList[i]['관리번호'] not in newManageList:
            todayDetailList.append(yesterdayDictList[i])
            
    updateDetailList = todayDetailList
     
    # 주인을 찾은 분실물은 유실물상태 -> Y
    # 주인을 찾지 못한 분실물은 유실물상태 -> N
    for i in range(len(updateDetailList)):
        if updateDetailList[i]['관리번호'] in deleteManageList:
            updateDetailList[i]['유실물상태'] = 'Y'
        else:
            updateDetailList[i]['유실물상태'] = 'N'
            
    jsonFilename = nowdate.strftime('%Y%m%d') + '_updateStatus'
    # hdfs
    hdfs = InsecureClient('http://59.187.205.37:9870')
    
    with open(f'{jsonFilename}.json','a') as file:
        json.dump(updateDetailList, file, ensure_ascii=False, indent=4)
    try:
        s3.upload_file(f'{jsonFilename}.json', "achachanew", f'updateStatus/{jsonFilename}.json')
        hdfs.write(f'/user/ubuntu/service_data/{jsonFilename}.json', data=updateDetailList, encoding='utf-8', overwrite=True)
    except Exception as err:
        print("input error", err)
        
    file_path = f'{jsonFilename}.json'

    if os.path.exists(file_path):
        os.remove(file_path)


