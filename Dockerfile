FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3 python3-pip software-properties-common && \
    pip3 install inflect pipenv

RUN add-apt-repository -y ppa:git-core/ppa && \
    apt-get install -y git && \
    git clone https://github.com/RobertBarrow/adventure.git && \
    chmod 0750 /adventure/adv.py && \
    ln -s /usr/bin/python3 /adventure/python

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /adventure
ENTRYPOINT ["/adventure/adv.py"]
