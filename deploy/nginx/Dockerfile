FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY site.conf /etc/nginx/conf.d/site.conf

# 避免与 site.conf 抢 80 端口；静态资源由 compose 挂载 dist
RUN rm -f /etc/nginx/conf.d/default.conf \
    && mkdir -p /usr/share/nginx/html
