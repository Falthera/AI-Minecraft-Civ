FROM node:20-slim

WORKDIR /app

COPY minecraft/client-bots/package*.json ./
RUN npm install --production

COPY minecraft/client-bots/ /app/

CMD ["npm", "start"]
