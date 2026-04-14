FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

# --host exposes Vite dev server on 0.0.0.0 so it's reachable outside the container
CMD ["npm", "run", "dev", "--", "--host"]
