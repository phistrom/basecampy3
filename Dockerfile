FROM python:3.9-slim

ARG USER_ID=2000
ARG GROUP_ID="${USER_ID}"
ARG USERNAME=basecampy
ARG WORKDIR=/bc3
ARG HOME_DIR="/home/${USERNAME}"

ENV WORKDIR="${WORKDIR}"
ENV HOME_DIR="${HOME_DIR}"
ENV BC3_OAUTH_BIND_ADDRESS=0.0.0.0
ENV BC3_CONTAINER=1
ENV BC3_CONFIG_PATH="/etc/basecamp.conf"
ENV PYTHONPATH="${WORKDIR}"

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR "${WORKDIR}"

COPY . .

RUN addgroup --gid ${GROUP_ID} "${USERNAME}" \
    && adduser --home "${HOME_DIR}" --gecos '' --uid "${USER_ID}" --gid "${GROUP_ID}" --disabled-password "${USERNAME}" \
    && ln -s "${WORKDIR}/bc3" "/usr/local/bin/bc3" \
    && touch "${BC3_CONFIG_PATH}" \
    && chown -R "${USERNAME}:${USERNAME}" "${WORKDIR}" "${BC3_CONFIG_PATH}"

RUN python setup.py install

USER ${USERNAME}

# for the bc3 configure command, it must listen on your localhost for
# the redirect URL to receive an authorization token
EXPOSE 33333

CMD ["bc3", "--help"]
