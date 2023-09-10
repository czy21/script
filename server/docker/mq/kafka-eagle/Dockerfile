FROM openjdk:11-jdk

ENV KE_VERSION=3.0.1
ENV KE_TGZ_URL=https://github.com/smartloli/kafka-eagle-bin/raw/v${KE_VERSION}/efak-web-${KE_VERSION}-bin.tar.gz

ENV KE_HOME=/opt/kafka-eagle
ENV PATH=$KE_HOME/bin:$PATH

RUN mkdir -p $KE_HOME
#COPY ___temp/efak-web-${KE_VERSION}-bin.tar.gz $KE_HOME/src.gz
RUN wget -nv -O $KE_HOME/src.gz $KE_TGZ_URL;
RUN tar -xf $KE_HOME/src.gz --strip-components=1 -C $KE_HOME && rm $KE_HOME/src.gz && chown -R root:root $KE_HOME

WORKDIR $KE_HOME

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]