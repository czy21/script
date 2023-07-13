FROM python:3.9.17-slim-bullseye as builder
WORKDIR /app

COPY requirements.txt mkdocs.yaml ./
COPY doc ./doc
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdocs build -d build/doc
RUN ls -al

FROM nginx:1.23.4-alpine
COPY --from=builder /app/build/doc /usr/share/nginx/html/
RUN ls -al /usr/share/nginx/html/