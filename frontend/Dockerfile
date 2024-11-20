# Stavebný krok (Build Stage)
FROM node:18-alpine AS build

WORKDIR /app

# Skopíruj package.json a package-lock.json
COPY package*.json ./

# Nainštaluj závislosti
RUN npm install

# Skopíruj zdrojové kódy a spusti build
COPY . .

WORKDIR /app/src

RUN npm run build

# Produkčný krok (Production Stage)
FROM nginx:alpine

# Skopíruj zostavené súbory z predchádzajúceho kroku
COPY --from=build /app/dist /usr/share/nginx/html

# Exponuj port 80
EXPOSE 80

# Spustenie NGINX
CMD ["nginx", "-g", "daemon off;"]
