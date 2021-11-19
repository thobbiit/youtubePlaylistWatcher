FROM python:3

ADD youtube_script.py /

RUN pip install google-api-python-client

CMD ["python", "./youtube_script.py"]

