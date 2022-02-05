FROM python:3.10-alpine

MAINTAINER TOPS gilson@tops.app.br

WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . /app

ENTRYPOINT [ "/usr/local/bin/python" ]
CMD [ "app.py" ]
