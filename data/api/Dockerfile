FROM node:16

WORKDIR /api

COPY package*.json .

RUN npm i

COPY . .

RUN ["npm", "run", "build"]

CMD ["npm", "run", "serve"]