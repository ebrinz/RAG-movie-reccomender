FROM node:16-alpine

WORKDIR /app

# Copy only package.json and package-lock.json first to leverage Docker caching
COPY src/ui/package.json src/ui/package-lock.json ./

RUN npm install

# Copy the rest of the frontend source code, including public and src
COPY src/ui ./

# Build the React app
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]