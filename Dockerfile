FROM python:3.8-slim-buster

ENV TINI_VERSION v0.19.0

RUN apt-get update -y && pip install -U pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /opt/app/

ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini

RUN chmod +x /tini && \
    useradd --create-home appuser

# STOPSIGNAL SIGINT

USER appuser
ENTRYPOINT ["/tini", "-s", "--"]

WORKDIR /opt/app

EXPOSE 5007

CMD ["gunicorn", "-w 1", "-b :5007", "server:APP"]
