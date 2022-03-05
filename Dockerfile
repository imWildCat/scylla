FROM node:lts-buster as node-build
WORKDIR /root
COPY package.json .
RUN yarn install
COPY . .
RUN make assets-build


FROM python:3.9-slim as python-build
RUN apt-get update && apt-get install -y g++ gcc libxslt-dev make libcurl4-openssl-dev build-essential
RUN apt-get install -y libssl-dev
WORKDIR /root

COPY --from=node-build /root/scylla/assets ./scylla/assets
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m playwright install
COPY . .
RUN python setup.py install

FROM python:3.9-slim as prod

LABEL maintainer="WildCat <wildcat.name@gmail.com>"

RUN apt-get update && apt-get install -y libxslt-dev libssl-dev libcurl4-openssl-dev

COPY --from=python-build /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=python-build /root/.cache/ms-playwright /root/.cache/ms-playwright

WORKDIR /var/www/scylla
VOLUME /var/www/scylla

EXPOSE 8899
EXPOSE 8081

CMD python -m scylla