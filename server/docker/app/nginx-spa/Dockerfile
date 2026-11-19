FROM nginx:1.31.9-alpine
RUN mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak
COPY ./nginx.conf /etc/nginx/conf.d/app.conf

WORKDIR /usr/share/nginx/html