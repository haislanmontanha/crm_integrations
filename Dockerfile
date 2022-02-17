FROM python:3.10-alpine

EXPOSE 5001

WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . /app

ENTRYPOINT [ "/usr/local/bin/python" ]
CMD [ "wsgi.py" ]
