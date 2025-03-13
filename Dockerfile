FROM python:3

WORKDIR /usr/src/checker_bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./
COPY credentials ./
COPY telegram_bot_token ./

CMD [ "python", "./main.py" ]
