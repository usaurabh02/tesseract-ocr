FROM python:3.9

RUN apt-get update \
  && apt-get -y install tesseract-ocr \
  && apt-get install -y python3 python3-distutils python3-pip \
  && apt-get install bash

COPY . /app 
WORKDIR /app

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt 

ENTRYPOINT ["python3"]
CMD ["app.py"]