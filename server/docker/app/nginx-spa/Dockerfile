FROM nginx:1.27.2-alpine
RUN mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak
COPY ./nginx.conf /etc/nginx/conf.d/app.conf

WORKDIR /usr/share/nginx/html