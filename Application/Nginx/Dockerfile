FROM nginx:1.22.1

# WORKDIR /etc/nginx/

# COPY nginx.conf /etc/nginx/sites-available/

# RUN mkdir -p /etc/nginx/sites-enabled/\
#     && ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/

COPY nginx.conf /etc/nginx/conf.d/

RUN mkdir -p /etc/nginx/conf.d/\
    && ln -s /etc/nginx/conf.d/nginx.conf

# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]