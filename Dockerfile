FROM nvidia/cuda:11.0.3-base-ubuntu20.04

COPY requirements.txt requirements.txt

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get -y install build-essential \
        zlib1g-dev \
        libncurses5-dev \
        libgdbm-dev \ 
        libnss3-dev \
        libssl-dev \
        libreadline-dev \
        libffi-dev \
        libsqlite3-dev \
        libbz2-dev \
        wget \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get purge -y imagemagick imagemagick-6-common 
RUN cd /usr/src \
    && wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz \
    && tar -xzf Python-3.11.0.tgz \
    && cd Python-3.11.0 \
    && ./configure --enable-optimizations \
    && make altinstall
RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.11 1
RUN apt-get install -y default-jre
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .

CMD [ "nvidia-smi" ]
RUN [ "chmod", "+x", "converter/fast-convert.jar" ]
CMD [ "python", "modifier.py"]
