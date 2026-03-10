#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UI_DEV_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SKILL_ROOT="$(cd "${UI_DEV_ROOT}/.." && pwd)"
SERVICE_NAME="meta-skill-docstructure-viewer.service"
USER_SYSTEMD_DIR="${HOME}/.config/systemd/user"
TARGET_FILE="${USER_SYSTEMD_DIR}/${SERVICE_NAME}"
PORT_VALUE="${PORT:-4178}"
TARGET_SKILL_ROOT_VALUE="${TARGET_SKILL_ROOT:-${SKILL_ROOT}}"

mkdir -p "${USER_SYSTEMD_DIR}"

sed \
  -e "s#__UI_DEV_ROOT__#${UI_DEV_ROOT}#g" \
  -e "s#__TARGET_SKILL_ROOT__#${TARGET_SKILL_ROOT_VALUE}#g" \
  -e "s#__PORT__#${PORT_VALUE}#g" \
  "${UI_DEV_ROOT}/assets/systemd/meta-skill-docstructure-viewer.service" > "${TARGET_FILE}"

systemctl --user daemon-reload
systemctl --user enable --now "${SERVICE_NAME}"
systemctl --user restart "${SERVICE_NAME}"

echo "Installed ${SERVICE_NAME} at ${TARGET_FILE}"
