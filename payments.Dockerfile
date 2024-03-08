FROM python:3.10

EXPOSE 5100/tcp

COPY payments-requirements.txt ./
RUN pip install --upgrade --no-cache-dir pip setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r payments-requirements.txt

COPY . .

WORKDIR "/src"

CMD [ "uvicorn", "payments.main:app", "--host", "localhost", "--port", "8001", "--reload"]