FROM python:3.10

EXPOSE 5000/tcp

COPY tenant-requirements.txt ./
RUN pip install --upgrade --no-cache-dir pip setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r tenant-requirements.txt

COPY . .

WORKDIR "/src"

CMD [ "uvicorn", "tenant.main:app", "--host", "localhost", "--port", "8000", "--reload"]