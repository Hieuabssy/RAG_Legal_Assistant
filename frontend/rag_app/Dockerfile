# Stage 1: Build the React application
FROM node:20-alpine as build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source code and build
COPY . .

RUN npm run build

# Stage 2: Serve the app with Nginx
FROM nginx:alpine
# Copy built assets to Nginx html folder
COPY --from=build /app/dist /usr/share/nginx/html
# (Optional) Copy custom nginx config if we use React Router
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
