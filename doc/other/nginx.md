#
```nginx
# 单域名 path区分多SPA应用 example: conf/app.conf
# SPA config 
#       publicPath: /admin/
#       router basename: /admin/

server {
    listen       80;
    server_name  app-dev.czy21-internal.com;
    
    location ^~/erp/ {
        proxy_pass http://127.0.0.1:8080/;
    }
    error_page   500 502 503 504  /50x.html;
    
    location = /50x.html {
        root   html;
    }
}

server {
    listen 8080;
    server_name 127.0.0.1;

    location / {
        root /usr/share/nginx/web/erp/;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass /;
        proxy_set_header   Host             $host;
        proxy_set_header   X-Real-IP        $remote_addr;
        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
        proxy_set_header  Upgrade          $http_upgrade;
        proxy_set_header  Connection       $http_connection;
    }
}
```