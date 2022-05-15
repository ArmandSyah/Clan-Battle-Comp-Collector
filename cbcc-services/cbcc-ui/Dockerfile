# pull oficial base image
FROM node:18-alpine

WORKDIR /usr/src/app

ENV PATH /usr/src/app/node_modules/.bin:$PATH   

COPY package.json .
COPY package-lock.json .
RUN npm ci
RUN npm install react-scripts@5.0.1 -g --silent

RUN mkdir -p node_modules/.cache && chmod -R 777 node_modules/.cache

# start app
CMD ["npm", "start"]
