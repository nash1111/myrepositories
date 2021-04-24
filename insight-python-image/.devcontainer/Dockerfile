FROM python:3.8-slim-buster

RUN apt update

RUN apt install make libssl-dev libghc-zlib-dev libcurl4-gnutls-dev libexpat1-dev gettext unzip -y \
    && apt install wget -y\
    && wget https://github.com/git/git/archive/v2.23.0.zip -O git.zip \
    && unzip git.zip \
    && cd git-* \
    && make prefix=/usr/local all \
    && make prefix=/usr/local install \
    && cd .. \
    && rm -rf git-* \
    && apt install openssh-client socat -y


# VOLUME .:/workspace:cached
# VOLUME ~/.ssh:/root/.ssh
# VOLUME ~/.gitconfig:/root/.gitconfig

# RUN ssh-keygen -t rsa -f /root/.ssh/id_rsa -q -P ""

#VOLUME ~/.ssh/id_rsa.pub:/root/.ssh/id_rsa.pub



RUN pip3 install autopep8 \
flake8 \
numpy==1.20.1 \
pandas==1.2.3 \
matplotlib==3.3.4 \
japanize-matplotlib==1.1.3 \
sklearn \
scipy==1.6.2 \
seaborn==0.11.1 \
pytest==6.2.2 \
pytest-cov==2.11.1