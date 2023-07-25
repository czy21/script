FROM fluent/fluentd:v1.16-debian
USER root

RUN gem install fluent-plugin-prometheus
RUN gem install fluent-plugin-elasticsearch -v 5.1.0
RUN gem uninstall elasticsearch elasticsearch-api elastic-transport --force -x
RUN gem install elasticsearch -v 7.17

USER fluent