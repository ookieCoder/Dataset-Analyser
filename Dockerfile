FROM node:20-alpine

WORKDIR /app

# Install dependencies based on the preferred package manager
COPY package.json package-lock.json ./
RUN npm ci

# Copy application source
COPY . .

# Set build-time environment variables
ARG NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
ENV NEXT_PUBLIC_BACKEND_URL=$NEXT_PUBLIC_BACKEND_URL

# Build Next.js
RUN npm run build

# Expose listening port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
