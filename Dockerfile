FROM registry.czy21-internal.com/library/mkdoc as builder
WORKDIR /app

COPY . .
RUN python3 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
RUN python3 main.py
RUN mkdocs build -d build/doc

FROM nginx:1.23.4-alpine
COPY --from=builder /app/build/doc /usr/share/nginx/html/