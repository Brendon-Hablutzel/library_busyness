FROM node:16 AS builder

WORKDIR /frontend

COPY package.json .
COPY package-lock.json .
RUN npm i

ARG REACT_APP_API_HOST
ARG REACT_APP_API_PORT

ENV REACT_APP_API_HOST=${REACT_APP_API_HOST}
ENV REACT_APP_API_PORT=${REACT_APP_API_PORT}

COPY . .

RUN npm run build

FROM nginx

COPY --from=builder /frontend/build /usr/share/nginx/html

COPY nginx.conf /etc/nginx/nginx.conf