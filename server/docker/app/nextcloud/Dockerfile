FROM nextcloud:stable-apache
RUN apt update
RUN apt install -y smbclient libsmbclient-dev
RUN pecl install smbclient
RUN docker-php-ext-enable smbclient