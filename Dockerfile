FROM ubuntu:22.04
LABEL maintainer="TBone <voss.till@gmail.com>"

RUN apt-get update \
  && apt-get install -y -qq tar git curl nano wget net-tools build-essential \
  && apt-get install -y -qq python3 python3-dev python3-setuptools \
  && apt-get install -y -qq python3-pip \
  && pip3 install --upgrade pip

COPY requirements.txt /flask/requirements_additional.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /flask/requirements_additional.txt

ADD Flask_backend /flask

EXPOSE 5000

WORKDIR /flask

CMD ["python3", "app.py"]