FROM flink:1.14-java11

COPY ./___temp/lib /opt/flink/lib/

RUN chown -R root:root .

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]