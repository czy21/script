FROM nginx:1.23.4-alpine
COPY ./doc.tar.gz /usr/share/nginx/
RUN tar -zxvf /usr/share/nginx/doc.tar.gz
RUN ls -al /usr/share/nginx/