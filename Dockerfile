FROM python:3.7
#FROM python:3.7-alpine

RUN adduser --disabled-password --gecos '' pyintro

RUN pip install pipenv

WORKDIR /home/pyintro
COPY Pipfile* ./

RUN pipenv install --system --deploy


COPY --chown=pyintro:pyintro bin/unix bin
RUN  chmod +x bin/*.sh

COPY --chown=pyintro:pyintro dev-python-intro dev-python-intro
COPY --chown=pyintro:pyintro config config

#ENV FLASK_APP nosqlpoc.py
#ENV VA_COMMAND api
ENV VA_COMMAND shell
ENV VA_SHELL_ARGS --

USER pyintro

EXPOSE 18080
ENTRYPOINT ["sh", "./bin/boot.sh"]
