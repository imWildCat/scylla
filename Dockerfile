FROM node:lts-buster as node-build

WORKDIR /root

COPY package.json .
RUN yarn install
COPY . .
RUN make assets-build

FROM ubuntu:focal as python-build

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Los_Angeles

RUN apt-get update && \
    apt-get install -y python3 python3-distutils libpython3.8-dev curl g++ gcc libxslt-dev make libcurl4-openssl-dev build-essential libssl-dev && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3 1 && \
    curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python get-pip.py && \
    rm get-pip.py && \
    # Feature-parity with node.js base images.
    apt-get install -y --no-install-recommends git openssh-client && \
    # clean apt cache
    rm -rf /var/lib/apt/lists/* && \
    # Create the pwuser
    adduser pwuser

WORKDIR /app

COPY --from=node-build /root/scylla/assets ./scylla/assets
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
RUN python3 setup.py install

RUN mkdir -p /var/www/scylla
VOLUME /var/www/scylla

RUN python3 -m playwright install chromium --with-deps

EXPOSE 8899
EXPOSE 8081

CMD python3 -m scylla --db-path /var/www/scylla/scylla.db
