FROM python:3.5-onbuild

ADD . /code
WORKDIR /code

CMD python run.py
