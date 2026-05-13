#!/bin/bash
# Wrapper for auto_deploy.py — ensures clean bash environment for cron runs
set -euo pipefail
cd /home/trevo/blog
python3 auto_deploy.py >> /home/trevo/blog/cron_deploy.log 2>&1