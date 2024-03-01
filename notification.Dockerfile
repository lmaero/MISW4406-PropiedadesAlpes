FROM python:3.10

COPY notification-requirements.txt ./
RUN pip install --no-cache-dir -r notification-requirements.txt

COPY . .

CMD [ "python", "./src/notifications/main.py" ]
