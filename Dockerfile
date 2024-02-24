FROM python:3.11.0-alpine

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
