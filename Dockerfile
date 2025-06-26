FROM ubuntu:22.04
LABEL maintainer="TBone <voss.till@gmail.com>"

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    ln -fs /usr/share/zoneinfo/Europe/Berlin /etc/localtime && \
    apt-get install -y tzdata && \
    dpkg-reconfigure -f noninteractive tzdata


RUN apt-get update && apt-get install -y -qq \
    tar git curl nano wget net-tools build-essential \
    python3 python3-dev python3-setuptools python3-pip \
    libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev \
    libopenjp2-7-dev libtiff-dev libwebp-dev \
    libffi-dev tcl-dev tk-dev \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt /flask/requirements_additional.txt

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r /flask/requirements_additional.txt

ADD Flask_backend /flask

EXPOSE 5000

WORKDIR /flask

CMD ["python3", "app.py"]
