FROM node:14.14-slim

WORKDIR /usr/src/app

ENV PATH /usr/src/app/node_modules/.bin:$PATH

COPY package.json .
COPY package-lock.json .
RUN npm install --production

COPY . .