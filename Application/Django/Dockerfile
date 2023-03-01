# Base image
FROM python:3.8.2

# 컨테이너 내에서 코드가 실행될 경로 설정
WORKDIR /home/ubuntu/docker

# apt 업데이트 및 업그레이드
RUN apt-get -y update && apt-get -y dist-upgrade

# vim 설치
RUN apt-get -y install vim 

# pip 설치 및 업그레이트
RUN apt-get install -y python3-pip
RUN pip install --upgrade pip

# 파이썬 패키지 설치
COPY requirements.txt .
RUN pip install --upgrade --no-deps --force-reinstall -r requirements.txt

# 프로젝트 코드를 /home/ubuntu/predict_gas로 복사
COPY . .

# 연결할 포트 번호
# EXPOSE 8000 

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "--bind" , "0.0.0.0:8000", "ACHACHA.wsgi:application"]
