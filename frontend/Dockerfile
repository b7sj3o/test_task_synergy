FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* .env ./
RUN npm install --no-audit --no-fund
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
RUN npm i -g serve
COPY --from=build /app/dist /app/dist
ENV PORT=5173
EXPOSE 5173
CMD ["npx", "vite", "preview", "--host", "0.0.0.0", "--port", "5173"]


