#!/usr/bin/env bash
set -euo pipefail

reviewdog -diff="git diff origin/develop"

./scripts/coverage/coverage.sh feature/size develop
