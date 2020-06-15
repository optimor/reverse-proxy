FROM ubuntu:20.04

# Enable non interactive mode to prevent any custom console questions asked
# during the packages installation
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get clean && \
    apt-get update && \
    apt-get install --no-install-recommends -y \
        build-essential \
        curl \
        git \
        locales \
        nginx \
        python3-dev \
        python3-pip \
        python3-setuptools \
        python3-virtualenv && \
    pip3 install --upgrade pip && \
    apt-get install --no-install-recommends -y \
      libxml2-dev \
      libxslt1-dev \
      zlib1g-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

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

ENV VIRTUAL_ENV_DIR /.venv
# Set the virtual environment as the main Python directory and make sure the
# custom python $PATH is persisted for users and bash sessions.
ENV PATH $VIRTUAL_ENV_DIR/bin:$PATH
RUN python3 -m virtualenv --python=python3 $VIRTUAL_ENV_DIR && \
    # Setup the bashrc for bash environment
    echo "PATH=$VIRTUAL_ENV_DIR/bin:$PATH" >> /root/.bashrc && \
    echo "PATH=$VIRTUAL_ENV_DIR/bin:$PATH" >> /home/django/.bashrc && \
    # Replace the default PATH value for 'su' usage. See more in the man page:
    # http://manpages.ubuntu.com/manpages/eoan/man1/su.1.html#config%20files
    sed -i "/^ENV_SUPATH/c\ENV_SUPATH    PATH=$PATH" /etc/login.defs && \
    sed -i "/^ENV_PATH/c\ENV_PATH      PATH=$PATH" /etc/login.defs && \
    # Replace the environment PATH for new su implementation (Ubuntu 20 up)
    sed -i "/^PATH/c\EPATH=\"$PATH\"" /etc/environment
RUN pip3 install pip-tools wheel

COPY ./requirements.txt $BACKEND_DIR/requirements.txt
RUN pip-sync $BACKEND_DIR/requirements.txt

COPY ./reverse_proxy $BACKEND_DIR
RUN /bin/bash -c "chown -R django:django $BACKEND_DIR"

RUN mkdir -p $LOG_DIR
RUN chown -R django:django $LOG_DIR

COPY ./entrypoint.sh /entrypoint.sh

EXPOSE 80
WORKDIR $BACKEND_DIR
ENTRYPOINT ["/entrypoint.sh"]
CMD ["$BACKEND_DIR/run.sh"]
