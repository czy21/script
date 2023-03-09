FROM flink:1.16.1-scala_2.12-java11
RUN chown -R root:root .
RUN sed -i 's|exec $(drop_privs_cmd) ||g' /docker-entrypoint.sh