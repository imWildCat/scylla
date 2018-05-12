FROM python:3.6-alpine3.7

RUN apk add --update --no-cache g++ gcc libxslt-dev

RUN mkdir -p /var/www/scylla
WORKDIR /var/www/scylla

RUN pip install scylla

CMD python -m scylla