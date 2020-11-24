FROM obolary-python-base

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG ENGINE
COPY ./algo/model.$ENGINE /usr/src/app
COPY ./XAUUSD_1M_ALL.csv /usr/src/app

RUN pip install -r requirements.txt

CMD [ "python", "agent.py", "--dataset_file", "./XAUUSD_1M_ALL.csv" ]
