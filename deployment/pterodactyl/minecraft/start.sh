#!/bin/bash
# Pterodactyl startup script for Minecraft server
set -e

# Ensure directories exist
mkdir -p /data/world /data/plugins /data/logs

# Accept EULA
echo "eula=true" > /data/eula.txt

# Start Paper server
exec java -Xmx${JAVA_XMX:-4G} -Xms${JAVA_XMS:-2G} -jar /data/server.jar nogui
