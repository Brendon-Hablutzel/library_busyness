FROM node:20.8.0

WORKDIR /api

COPY package*.json .

RUN npm i

COPY tsconfig.json .
COPY src src

RUN ["npm", "run", "build"]

CMD ["node", "dist/index.js"]