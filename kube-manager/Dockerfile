FROM centos:7

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN yum update -y
RUN yum -y install epel-release && yum clean all
RUN yum -y install python-pip && yum clean all
RUN yum -y install openssl
RUN yum install -y vim
RUN yum install -y redis
RUN pip install kubernetes
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN yum -y install wget
ADD . /code/
COPY entrypoint.sh /code/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/code/entrypoint.sh"]

