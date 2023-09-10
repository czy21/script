FROM openjdk:11-jre-slim

ENV PULSAR_MANAGER_VERSION=0.2.0
ENV PULSAR_MANAGER_TGZ_URL=https://dist.apache.org/repos/dist/release/pulsar/pulsar-manager/pulsar-manager-${PULSAR_MANAGER_VERSION}/apache-pulsar-manager-${PULSAR_MANAGER_VERSION}-bin.tar.gz
ENV PULSAR_MANAGER_HOME=/opt/pulsar-manager
ENV PATH=${PULSAR_MANAGER_HOME}/bin:$PATH

COPY sources.list /etc/apt/

RUN apt-get update

RUN apt-get install --yes nginx wget \
 && rm -rf /tmp/* \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir -p ${PULSAR_MANAGER_HOME}
#COPY ___temp/apache-pulsar-manager-${PULSAR_MANAGER_VERSION}-bin.tar.gz ${PULSAR_MANAGER_HOME}/src.tgz
RUN wget -nv -O ${PULSAR_MANAGER_HOME}/src.tgz ${PULSAR_MANAGER_TGZ_URL};
RUN tar -xf ${PULSAR_MANAGER_HOME}/src.tgz --strip-components=1 -C ${PULSAR_MANAGER_HOME} \
 && tar -xf ${PULSAR_MANAGER_HOME}/pulsar-manager.tar --strip-components=1 -C ${PULSAR_MANAGER_HOME} \
 && rm ${PULSAR_MANAGER_HOME}/src.tgz && chown -R root:root ${PULSAR_MANAGER_HOME}

RUN cp -r ${PULSAR_MANAGER_HOME}/dist/* /usr/share/nginx/html/
RUN rm -rf ${PULSAR_MANAGER_HOME}/LICENSE ${PULSAR_MANAGER_HOME}/NOTICE ${PULSAR_MANAGER_HOME}/dist ${PULSAR_MANAGER_HOME}/pulsar-manager.tar ${PULSAR_MANAGER_HOME}/licenses

COPY conf/nginx.conf /etc/nginx/conf.d/default.conf

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]