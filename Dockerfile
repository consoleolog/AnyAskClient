FROM python:3.10

WORKDIR /app

RUN pip install --upgrade pip

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./


EXPOSE 8501

CMD ["streamlit", "run", "app.py"]