#!/bin/bash
# SessionStart hook — tự kết nối tới danangmobile.com mỗi phiên Claude Code.
# KHÔNG chứa khoá bí mật: chỉ đọc từ Environment variables (web) rồi sinh .env.
# Yêu cầu: đặt WP_SITE, WP_USER, WP_APP_PASSWORD trong Environment variables.
set -uo pipefail

ENV_DIR="${CLAUDE_PROJECT_DIR:-.}/seo-tools"
[ -d "$ENV_DIR" ] || exit 0

if [ -n "${WP_SITE:-}" ] && [ -n "${WP_USER:-}" ] && [ -n "${WP_APP_PASSWORD:-}" ]; then
  umask 077
  printf 'WP_SITE=%s\nWP_USER=%s\nWP_APP_PASSWORD=%s\n' \
    "$WP_SITE" "$WP_USER" "$WP_APP_PASSWORD" > "$ENV_DIR/.env"
  echo "[session-start] Đã tạo seo-tools/.env từ Environment variables."
  ( cd "$ENV_DIR" && python3 publish_wp.py --check 2>&1 | head -3 ) \
    || echo "[session-start] Kết nối WP thất bại — kiểm tra lại WP_APP_PASSWORD."
else
  echo "[session-start] Thiếu WP_SITE/WP_USER/WP_APP_PASSWORD trong Environment variables → bỏ qua tạo .env."
fi
exit 0
