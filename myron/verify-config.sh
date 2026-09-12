#!/usr/bin/env bash
set -euo pipefail
# 检查 Image 中提取出的实际配置；缺失或被依赖覆盖都中止构建。
for key in PID_NS IPC_NS SYSVIPC POSIX_MQUEUE DEVTMPFS USER_NS MODULES ARM64_4K_PAGES IKCONFIG; do
  grep -qx "CONFIG_${key}=y" "$1" || { echo "缺少 CONFIG_${key}=y" >&2; exit 1; }
done
if grep -Eq '^CONFIG_(KSU(_[A-Z0-9_]+)?|ARM64_16K_PAGES|ARM64_64K_PAGES)=(y|m)$' "$1"; then
  echo "检测到不允许的 KSU 或页面大小配置" >&2
  exit 1
fi
