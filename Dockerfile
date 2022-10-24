FROM python:3.10.4

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

EXPOSE ${APP_PORT}

CMD ["python", "-m", "example_api"]
