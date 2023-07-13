FROM nginx:1.23.4-alpine
COPY ./build/doc /usr/share/nginx/html/