FROM python:3.7

WORKDIR /app

COPY ["requirements.txt", "./"]

RUN pip install -r requirements.txt

COPY ["kueski_mle_task", "./kueski_mle_task"]

ENTRYPOINT ["python",  "kueski_mle_task/run.py"]