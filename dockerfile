FROM ubuntu:20.04

# Create directories app_home and static directories
WORKDIR /app

RUN apt update
RUN apt-get install -y openjdk-8-jre
RUN apt-get install -y openjfx

CMD java -Xmx6000m -jar custom.jar
