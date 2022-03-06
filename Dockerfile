FROM node:lts-buster as node-build
WORKDIR /root
COPY package.json .
RUN yarn install
COPY . .
RUN make assets-build

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Los_Angeles

FROM ubuntu:focal as python-build
RUN apt-get update && \
    # Install Python
    apt-get install -y python3 python3-distutils curl g++ gcc libxslt-dev make libcurl4-openssl-dev build-essential libssl-dev && \
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

COPY --from=node-build /root/scylla/assets ./scylla/assets
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python setup.py install

FROM ubuntu:focal as prod
# From: https://github.com/microsoft/playwright-python/blob/main/utils/docker/Dockerfile.focal

LABEL maintainer="WildCat <wildcat.name@gmail.com>"

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Los_Angeles

RUN apt-get update && \
    # Install Python
    apt-get install -y python3 python3-distutils curl libxslt-dev libssl-dev libcurl4-openssl-dev && \
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

COPY --from=python-build /root/.local/lib/python3.8/site-packages/ /root/.local/lib/python3.8/site-packages/

WORKDIR /var/www/scylla
VOLUME /var/www/scylla

RUN echo $(python -m site --user-site)
RUN echo $(python --version)

RUN python -m playwright install chromium --with-deps

EXPOSE 8899
EXPOSE 8081

CMD python -m scylla