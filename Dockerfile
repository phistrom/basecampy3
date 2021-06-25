FROM python:3.9-alpine

ARG USER_ID=2000
ARG GROUP_ID="${USER_ID}"
ARG USERNAME=basecampy
ARG USER_HOME=/bc3
ARG WORKDIR=${USER_HOME}

ENV WORKDIR="${WORKDIR}"
ENV BC3_OAUTH_BIND_ADDRESS=0.0.0.0
ENV BC3_CONTAINER=1

# temporarily switch to this directory to copy our source code into and install
WORKDIR /usr/src/app
COPY . .

RUN python setup.py install \
    && addgroup -g "${GROUP_ID}" "${USERNAME}" \
    && adduser -u "${USER_ID}" -G ${USERNAME} -h "${USER_HOME}" -s /bin/sh -D "${USERNAME}" \
    && mkdir -p "${WORKDIR}" \
    && mkdir -p "${USER_HOME}/.config" \
    && chown -R "${USERNAME}:${USERNAME}" "${WORKDIR}" "${USER_HOME}"

USER ${USERNAME}
WORKDIR ${WORKDIR}

# persist this location if you want to keep your
# credentials when recreating the container
VOLUME ["${USER_HOME}/.config"]

# for the bc3 configure command, it must listen on your localhost for
# the redirect URL to receive an authorization token
EXPOSE 33333

ENTRYPOINT ["bc3"]
CMD ["--help"]
