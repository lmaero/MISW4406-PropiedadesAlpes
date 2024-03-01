FROM python:3.10

EXPOSE 6000/tcp

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "flask", "--app", "./src/pda/api", "run", "--host=0.0.0.0"]
