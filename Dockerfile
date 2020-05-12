FROM python:3.8.2-alpine3.10
WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir pynav2

COPY pynav2/. pynav2/
COPY pynav2.egg-info/ ./
COPY setup.py ./
COPY INSTALL ./
COPY MANIFEST.in ./

CMD ["python"]
