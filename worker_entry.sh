#!/bin/sh
set -e
# ينتظر اتصال ريديس في حالات التطوير
sleep 2
exec rq worker -u "$REDIS_URL" default
