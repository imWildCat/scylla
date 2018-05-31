FROM python:3.6.5-slim as build

RUN apt-get update && apt-get install -y g++ gcc libxslt-dev make libcurl4-openssl-dev build-essential

RUN apt-get install -y libssl-dev

RUN mkdir -p /var/www/scylla
WORKDIR /var/www/scylla

RUN pip install scylla

FROM python:3.6.5-slim

LABEL maintainer="WildCat <wildcat.name@gmail.com>"

RUN apt-get update && apt-get install -y libxslt-dev libssl-dev libcurl4-openssl-dev

RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget

COPY --from=build /usr/local/lib/python3.6/site-packages/ /usr/local/lib/python3.6/site-packages/

WORKDIR /var/www/scylla
VOLUME /var/www/scylla

EXPOSE 8899
EXPOSE 8081

CMD python -m scylla