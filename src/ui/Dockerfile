FROM node:16-alpine

WORKDIR /app

# Copy package.json and package-lock.json
COPY src/ui/package.json src/ui/package-lock.json ./

# Install dependencies, including dev dependencies
RUN npm install

# Copy the entire project
COPY src/ui ./

# Expose the React app development server port
EXPOSE 3000

# Use Nodemon in development mode
CMD ["npm", "run", "start:dev"]