FROM flink:1.14.4-scala_2.11-java11

RUN chown -R root:root .

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]