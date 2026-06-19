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

API_URL="https://api.github.com/repos/kubernetes-sigs/cloud-provider-kind/releases/latest"

# Authentification optionnelle pour éviter le rate-limit de l'API GitHub
# (60 req/h en anonyme, 5000 req/h avec un token).
CURL_AUTH=()
if [[ -n "${GITHUB_TOKEN:-}" ]]; then
    CURL_AUTH=(-H "Authorization: Bearer ${GITHUB_TOKEN}")
fi

RELEASE_JSON="$(curl -fsSL "${CURL_AUTH[@]}" "${API_URL}")"
if [[ $? -ne 0 || -z "${RELEASE_JSON}" ]]; then
    echo "Erreur: impossible de récupérer la release depuis l'API GitHub (réseau ou rate-limit ?)." >&2
    exit 1
fi

# Vérifie que la réponse est bien du JSON exploitable avant de l'utiliser.
if ! echo "${RELEASE_JSON}" | jq -e '.assets' >/dev/null 2>&1; then
    MSG="$(echo "${RELEASE_JSON}" | jq -r '.message // empty' 2>/dev/null)"
    echo "Erreur: réponse inattendue de l'API GitHub${MSG:+ : ${MSG}}." >&2
    echo "Astuce: définissez GITHUB_TOKEN pour augmenter la limite de requêtes." >&2
    exit 1
fi

KIND_CLOUD_SRC="$(echo "${RELEASE_JSON}" | jq -r --arg os "${OSTYPE}" --arg cpu "${GH_CPUTYPE}" \
    '.assets[] | select(.name | contains($os)) | select(.name | contains($cpu)) | .browser_download_url')"

if [[ -z "${KIND_CLOUD_SRC}" ]]; then
    echo "Erreur: aucun asset trouvé pour ${OSTYPE}/${GH_CPUTYPE}." >&2
    exit 1
fi
echo "${KIND_CLOUD_SRC}"

mkdir -p "${BIN_DEST}"
curl -fsSL "${KIND_CLOUD_SRC}" | tar -xz -C "${BIN_DEST}" "${BIN_NAME}"
