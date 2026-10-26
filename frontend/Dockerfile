# ---------- Etapa 1: compilar React ----------
FROM node:22-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

# Vite incrusta esta variable al compilar. "/api" = nginx redirige al backend
ARG VITE_API_URL=/api
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

# ---------- Etapa 2: servir con nginx ----------
FROM nginx:1.27-alpine

ENV BACKEND_HOST=backend \
    BACKEND_PORT=8000

# nginx reemplaza ${BACKEND_HOST} y ${BACKEND_PORT} al arrancar
COPY nginx.conf /etc/nginx/templates/default.conf.template
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80