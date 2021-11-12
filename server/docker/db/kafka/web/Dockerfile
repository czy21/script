FROM openjdk:11-jdk

RUN apt-get update;
ENV KE_VERSION=2.0.8
ENV KAFKA_TGZ_URL=https://github.com/smartloli/kafka-eagle-bin/archive/v${KE_VERSION}.tar.gz
ENV KE_HOME=/opt/kafka-eagle
ENV PATH=$KE_HOME/bin:$PATH

RUN set -ex; \
    mkdir -p $KE_HOME; \
    wget -nv -O $KE_HOME/src.tgz $KAFKA_TGZ_URL; \
    tar -xf $KE_HOME/src.tgz --strip-components=1 -C $KE_HOME; \
    mv $KE_HOME/efak-web-${KE_VERSION}-bin.tar.gz $KE_HOME/src.tgz; \
    tar -xf $KE_HOME/src.tgz --strip-components=1 -C $KE_HOME; \
    ls -al $KE_HOME; \
    rm $KE_HOME/src.tgz;

WORKDIR $KE_HOME

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]