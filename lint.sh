set -e

pycodestyle symbiflow
pylint -s n symbiflow
git diff --check --cached
