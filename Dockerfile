FROM python:3.5-onbuild

ADD . /code
WORKDIR /code
# RUN pip install -r requirements.txt
CMD python run.py
