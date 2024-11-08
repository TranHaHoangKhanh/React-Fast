# Use Node.js as the base image - choose LTS version for stability
FROM node:lts-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json first to leverage Docker cache
COPY package*.json /app

# Install dependencies
RUN npm install

# Copy the rest of your application code
COPY . .

# Build the React application for production
RUN npm run build

# Install a lightweight server to serve the static files
RUN npm install -g serve

# Expose port 3000 - default port for React applications
EXPOSE 3000

# Command to serve the built application
CMD ["npm", "start"]