FROM python:3.10

WORKDIR /app

# 필수 패키지 설치
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx gcc g++ libc-dev && \
    rm -rf /var/lib/apt/lists/*

# pip 업그레이드
RUN pip install --upgrade pip

# requirements.txt 복사 및 설치
COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일 복사
COPY ./ ./

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
