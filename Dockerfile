from ubuntu:16.04

MAINTAINER Marcin Kawa kawa.macin@gmail.com

RUN apt-get clean && \
    apt-get update && \
    apt-get -y install \
        locales \
        curl \
        git \
        nginx \
        python3-dev \
        python3-setuptools \
        python3-pip && \
    pip3 install --upgrade pip

RUN apt-get install -y libxml2-dev libxslt1-dev zlib1g-dev

# Set the locale
RUN locale-gen en_GB.UTF-8
ENV LANG en_GB.UTF-8
ENV LC_ALL en_GB.UTF-8
ENV ENVIRONMENT development
ENV BACKEND_DIR /src
ENV LOG_DIR /var/log/optimor/reverse_proxy
ENV LOG_FILE_DJANGO $LOG_DIR/app_django.log

RUN /bin/bash -c "ln -s $(which python3) /usr/bin/python" && \
    /bin/bash -c "mkdir -p $BACKEND_DIR" && \
    adduser --disabled-password --gecos "" django
WORKDIR $BACKEND_DIR

COPY ./requirements.txt $BACKEND_DIR/requirements.txt
RUN /bin/bash -c "pip3 install -r $BACKEND_DIR/requirements.txt"

COPY ./reverse_proxy $BACKEND_DIR
RUN /bin/bash -c "chown -R django:django $BACKEND_DIR"

RUN mkdir -p $LOG_DIR
RUN chown -R django:django $LOG_DIR

COPY ./entrypoint.sh /entrypoint.sh

EXPOSE 80
WORKDIR $BACKEND_DIR
ENTRYPOINT ["/entrypoint.sh"]
CMD ["$BACKEND_DIR/run.sh"]
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
