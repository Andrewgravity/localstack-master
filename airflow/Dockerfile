FROM apache/airflow:2.5.1
COPY ./requirements.txt ./requirements.txt
RUN pip install --requirement ./requirements.txt

USER root
RUN apt update && \
    apt install -y openjdk-11-jdk && \
    apt clean

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64