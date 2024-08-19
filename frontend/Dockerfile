FROM node:lts-alpine AS build-stage

WORKDIR /app

ENV PATH=/app/node_modules/.bin:$PATH

COPY package.json .
RUN npm install

COPY . .

EXPOSE 8080

CMD ["npm", "run", "dev"]
