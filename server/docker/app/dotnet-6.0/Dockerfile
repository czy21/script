FROM mcr.microsoft.com/dotnet/sdk:6.0.428-1-jammy

WORKDIR /app

ENV API_FILE=/app/api

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8080
ENTRYPOINT ["/docker-entrypoint.sh"]