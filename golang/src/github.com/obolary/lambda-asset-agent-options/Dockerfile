FROM obolary-python-base as data

WORKDIR /usr/src/app

COPY ./XAUUSD_1M_ALL.csv /usr/src/app

FROM data

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG ENGINE
COPY ./algo/model.$ENGINE /usr/src/app

RUN pip install -r requirements.txt

CMD [ "python", "agent.py", "--dataset_file", "./XAUUSD_1M_ALL.csv" ]
