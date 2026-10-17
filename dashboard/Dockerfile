FROM node:22-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

ARG VERSION=dev
ENV VITE_BUILD_VERSION=${VERSION}

RUN printf '{"version":"%s"}\n' "$VERSION" > public/version.json \
    && npm run build

FROM nginx:alpine

COPY --from=builder /app/dist/ /usr/share/nginx/html/
COPY default.conf.template /etc/nginx/templates/default.conf.template

EXPOSE 80