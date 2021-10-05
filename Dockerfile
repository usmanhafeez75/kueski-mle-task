FROM python:3.7

WORKDIR /app

COPY ["kueski_mle_task", "./kueski_mle_task"]

COPY ["requirements.txt", "setup.py", "./"]

RUN pip install .

ENTRYPOINT ["python",  "kueski_mle_task/run.py"]