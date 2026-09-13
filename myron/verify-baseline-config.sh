#!/usr/bin/env bash
set -euo pipefail
# 基线保留 AOSP 配置，不启用容器特性；检查实际 Image 配置。
for key in MODULES ARM64_4K_PAGES IKCONFIG; do
  grep -qx "CONFIG_${key}=y" "$1" || { echo "缺少 CONFIG_${key}=y" >&2; exit 1; }
done
for key in SYSVIPC POSIX_MQUEUE USER_NS PID_NS DEVTMPFS TMPFS_POSIX_ACL TMPFS_XATTR; do
  grep -qx "# CONFIG_${key} is not set" "$1" ||
    { echo "基线配置不符：CONFIG_${key} 应关闭" >&2; exit 1; }
done
if grep -Eq '^CONFIG_(IPC_NS|KSU(_[A-Z0-9_]+)?|ARM64_16K_PAGES|ARM64_64K_PAGES)=(y|m)$' "$1"; then
  echo '检测到非预期的 namespace、KSU 或页面大小配置' >&2
  exit 1
fi
