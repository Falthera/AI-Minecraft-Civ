FROM eclipse-temurin:21-jre

RUN apt-get update && apt-get install -y curl mcstatus && rm -rf /var/lib/apt/lists/*

# Paper 1.21.11 setup
ENV PAPER_VERSION=1.21.11
RUN mkdir -p /data/plugins /data/world

COPY --from=ghcr.io/papermc/paper:${PAPER_VERSION} /papermc.jar /data/server.jar
COPY minecraft/plugin/target/ai-civilization-plugin-1.0.0.jar /data/plugins/

COPY deployment/docker/minecraft/server.properties /data/server.properties
COPY deployment/docker/minecraft/paper-world-settings.yaml /data/paper-world-settings.yaml
COPY deployment/docker/minecraft/bukkit.yml /data/bukkit.yml
COPY deployment/docker/minecraft/spigot.yml /data/spigot.yml

WORKDIR /data

EXPOSE 25565

CMD ["java", "-Xmx${JAVA_XMX:-4G}", "-Xms${JAVA_XMS:-2G}", "-jar", "server.jar", "nogui"]
