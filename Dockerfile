FROM registry.czy21-internal.com/library/mkdoc as builder
WORKDIR /app

COPY . .
RUN python3 -m pip install -r requirements.txt -i http://nexus.czy21-internal.com/repository/pypi-proxy/simple/ --trusted-host nexus.czy21-internal.com
RUN git clone http://gitea.czy21-internal.com/czyhome/container
RUN python3 main.py
RUN mkdocs build -d build/doc

FROM nginx:1.23.4-alpine
COPY --from=builder /app/build/doc /usr/share/nginx/html/