FROM gnosko-python-api

RUN apt-get update
RUN apt-get -y install git

WORKDIR /usr/src/lib

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /usr/src/lib/td-ameritrade-python-gym

RUN pip install --upgrade pip
RUN pip install -e td-ameritrade-python-gym
RUN pip install -e git+https://github.com/obolary/td-ameritrade-python-api.git@develop#egg=td-ameritrade-python-api
RUN pip install -e git+https://github.com/obolary/option-pricing-python.git@develop#egg=option-pricing-python

