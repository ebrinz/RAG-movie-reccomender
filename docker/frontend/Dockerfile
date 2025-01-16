FROM node:16-alpine

WORKDIR /app

# Copy package files and install dependencies from the frontend directory
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

# Copy the entire frontend source code
COPY frontend/ .

RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]