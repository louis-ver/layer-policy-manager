# Usage:
# docker run \
#     -it \
#     --rm \
#     -v /Users/<user>/.aws/credentials:/root/.aws/credentials \
#     layer-policy-manager [OPTIONS]

FROM python:3.8-alpine

WORKDIR /usr/src/layer-policy-manager

COPY setup.py .
COPY layer_policy.py .

RUN pip3 install .

ENTRYPOINT [ "layer-policy-manager" ]