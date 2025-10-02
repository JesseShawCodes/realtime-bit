FROM node:20

# WORKDIR setup in Docker Container
WORKDIR /app

# Copy over package.json package-lock.json files. If new packages are added, npm i should run outside of container to update
COPY package.json package-lock.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]