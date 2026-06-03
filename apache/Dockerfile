FROM owasp/modsecurity-crs:apache

USER root

# 1. Copiamos tus archivos estáticos (frontend) al directorio web del contenedor
COPY ./static/ /var/www/html
RUN chmod -R 755 /var/www/html

# 2. Copiamos tu configuración a la ruta REAL de VirtualHosts de esta imagen
COPY demo.apache.conf /usr/local/apache2/conf/extra/httpd-vhosts.conf