FROM python:3
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdocs build

FROM nginx:1.23.4-alpine
COPY --from=builder /app/build/doc /usr/share/nginx/html/
RUN ls -al /usr/share/nginx/html/