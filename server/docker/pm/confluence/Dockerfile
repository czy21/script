FROM cptactionhank/atlassian-confluence:latest

USER root

COPY ./.tmp/atlassian-agent.jar /opt/atlassian/confluence/
COPY ./.tmp/lib/ /opt/atlassian/confluence/lib/

RUN echo 'export CATALINA_OPTS="-javaagent:/opt/atlassian/confluence/atlassian-agent.jar ${CATALINA_OPTS}"' >> /opt/atlassian/confluence/bin/setenv.sh