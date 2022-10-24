FROM python:3.10.4

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./

EXPOSE ${APP_PORT}

CMD ["python", "-m", "test_api"]
