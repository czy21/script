FROM registry.czy21-internal.com/library/mkdoc as builder
WORKDIR /app

COPY mkdocs.yaml ./
COPY doc ./doc
RUN mkdocs build -d build/doc

FROM nginx:1.23.4-alpine
COPY --from=builder /app/build/doc /usr/share/nginx/html/