FROM {{ param_registry }}/{{ param_registry_dir }}/hadoop-base

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
EXPOSE 22 9870 9000
ENTRYPOINT ["/docker-entrypoint.sh"]
