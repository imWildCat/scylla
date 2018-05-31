FROM python:3.6-alpine3.7 as build

RUN apk add --update --no-cache g++ gcc libxslt-dev make build-base curl-dev openssl-dev

RUN mkdir -p /var/www/scylla
WORKDIR /var/www/scylla

RUN pip install scylla

FROM python:3.6-alpine3.7

LABEL maintainer="WildCat <wildcat.name@gmail.com>"

RUN apk add --update --no-cache libxslt-dev

COPY --from=build /usr/local/lib/python3.6/site-packages/ /usr/local/lib/python3.6/site-packages/

WORKDIR /var/www/scylla
VOLUME /var/www/scylla

EXPOSE 8899
EXPOSE 8081

CMD python -m scylla
