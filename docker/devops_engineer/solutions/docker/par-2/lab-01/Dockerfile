# Stage 1: Builder (Install dependencies & build the app)
FROM node:18-alpine AS builder
RUN echo "Build stage has started 🚀"
WORKDIR /app
COPY package.json ./
# RUN npm install  --only=production
RUN npm install
COPY . .
RUN echo "Build stage has finished ✅"

# Stage 2: Tester (Run tests separately)
FROM node:18-alpine AS tester
RUN echo "Test stage has started 🚀"
WORKDIR /app
COPY --from=builder /app/package.json ./
RUN npm install         # Installs all dependencies
COPY . .
RUN npm test            # If tests fail, the build will stop here
RUN echo "Test stage has finished ✅"

# Stage 3: Production (Final lightweight image)
FROM node:18-alpine AS production
WORKDIR /app
RUN echo "Final-image stage has started 🚀"
# Now, copy from the tester stage to ensure tests were run successfully
COPY --from=tester /app/node_modules ./node_modules
COPY --from=tester /app/server.js .
# ENV NODE_ENV=production
EXPOSE 3000
RUN echo "Final-image stage has finished ✅"
CMD ["node", "server.js"]
