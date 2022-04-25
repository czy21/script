FROM apachepulsar/pulsar-manager:v0.2.0

RUN chown -R root:root /pulsar-manager

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]