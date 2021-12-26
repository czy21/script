FROM cptactionhank/atlassian-jira-software:latest

USER root

COPY ./___temp/atlassian-agent.jar /opt/atlassian/jira/
COPY ./___temp/lib/ /opt/atlassian/jira/lib/

RUN echo 'export CATALINA_OPTS="-javaagent:/opt/atlassian/jira/atlassian-agent.jar ${CATALINA_OPTS}"' >> /opt/atlassian/jira/bin/setenv.sh