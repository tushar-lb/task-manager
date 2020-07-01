FROM python:3.8

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /code/
COPY entrypoint.sh /code/entrypoint.sh

RUN apt-get update -y && apt-get install -y apt-transport-https
RUN curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
RUN echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | tee -a /etc/apt/sources.list.d/kubernetes.list
RUN apt-get update -y
RUN apt-get install -y kubectl
RUN apt-get install dnsutils -y

EXPOSE 8000

ENTRYPOINT ["/code/entrypoint.sh"]

