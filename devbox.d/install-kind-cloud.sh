#!/bin/env bash
OSTYPE="$(uname -s | tr -d '0-9.' | tr '[:upper:]' '[:lower:]')"
CPUTYPE="$(uname -m)"
BIN_DEST=${DEVBOX_PROJECT_ROOT}/.devbox/bin/
BIN_NAME="cloud-provider-kind"

if [[ -f ${BIN_DEST}/${BIN_NAME} ]]; then
    echo "already installed"
    exit 0;
fi

case "${CPUTYPE}" in
    aarch64|arm64)
    GH_CPUTYPE="arm64";;
    x86_64)
    GH_CPUTYPE="amd64" ;;
    *)
    echo '??' ;;
esac

KIND_CLOUD_SRC=$(curl -s https://api.github.com/repos/kubernetes-sigs/cloud-provider-kind/releases/latest  |  jq -r '.assets[] | select(.name | contains ("'${OSTYPE}'")) | select(.name | contains ("'${GH_CPUTYPE}'"))  | .browser_download_url')
echo ${KIND_CLOUD_SRC}

mkdir -p ${BIN_DEST}
curl -L ${KIND_CLOUD_SRC} | tar -xz -C ${BIN_DEST} ${BIN_NAME}
