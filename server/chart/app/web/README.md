## nginx.conf for app
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}
  namespace: {{ .Release.Namespace }}
  labels:
    app: {{ .Release.Name }}
data:
  nginx.conf: |
    user  nginx;
    worker_processes  auto;

    error_log  /dev/stderr;
    pid        /var/run/nginx.pid;

    events {
        worker_connections  1024;
    }

    http {
        include       /etc/nginx/mime.types;
        default_type  application/octet-stream;

        log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                          '$status $body_bytes_sent "$http_referer" '
                          '"$http_user_agent" "$http_x_forwarded_for"';

        access_log  /dev/stdout;

        sendfile        on;
        #tcp_nopush     on;

        keepalive_timeout  65;

        #gzip  on;

        server {
            listen       80;
            server_name  127.0.0.1;

            location / {
                root /usr/share/nginx/web/;
                index index.html;
                try_files $uri $uri/ /index.html;
            }

            location /api/ {
                proxy_pass {{ .Values.backend_url }}/;
                proxy_set_header   Host             $host;
                proxy_set_header   X-Real-IP        $remote_addr;
                proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
                #proxy_set_header  Upgrade          $http_upgrade;
                #proxy_set_header  Connection       $http_connection;
            }

            error_page   500 502 503 504  /50x.html;
            
            location = /50x.html {
                root   html;
            }

        }
    }
    stream {
        
    }
```