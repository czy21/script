FROM mcr.microsoft.com/dotnet/aspnet:7.0
WORKDIR /app

ENV DLL=/app/api.dll

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

VOLUME ["/app/conf/","/app/data/"]
EXPOSE 8080
ENTRYPOINT ["/docker-entrypoint.sh"]