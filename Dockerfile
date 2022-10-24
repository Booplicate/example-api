FROM python:3.10.4

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./

EXPOSE 5050

CMD ["python", "-m", "test_api", "0.0.0.0", "5050"]
