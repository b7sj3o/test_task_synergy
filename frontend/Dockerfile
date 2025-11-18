FROM node:16-alpine

EXPOSE 5173
WORKDIR /app

COPY package.json .
RUN npm install

COPY . .

RUN npm run build

CMD ["npx", "vite", "preview", "--host", "0.0.0.0", "--port", "5173"]