FROM ubuntu:20.04

# Create directories app_home and static directories
WORKDIR /app

RUN apt update
RUN apt-get install -y openjdk-8-jre
RUN apt-get install -y openjfx

COPY libraries libraries
COPY mods mods
COPY plugins plugins
COPY custom.jar custom.jar
COPY eula.txt eula.txt
COPY minecraft_server.1.7.10.jar minecraft_server.1.7.10.jar
COPY server.properties server.properties

COPY help.yml help.yml
COPY commands.yml commands.yml
COPY ops.json ops.json
COPY permissions.yml permissions.yml
COPY spigot.yml spigot.yml
COPY tileentities.yml tileentities.yml
COPY usercache.json usercache.json
COPY usernamecache.json usernamecache.json
COPY wepif.yml wepif.yml
COPY whitelist.json whitelist.json
COPY banned-players.json banned-players.json
COPY banned-ips.json banned-ips.json

CMD java -Xmx3500m -jar custom.jar
