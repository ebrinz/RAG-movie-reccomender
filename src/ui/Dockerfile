FROM node:16-alpine

WORKDIR /app

# Copy package.json and package-lock.json
COPY src/ui/package*.json ./

# Install ALL dependencies, including dev dependencies
RUN npm install --include=dev

# Copy the entire project
COPY src/ui .

EXPOSE 3000

CMD ["npm", "run", "start:dev"]