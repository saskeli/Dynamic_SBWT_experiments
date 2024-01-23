#!/bin/bash
set -euxo pipefail

bash install_apt_dependencies.sh
bash install_bifrost.sh
bash install_bufboss.sh
bash install_dynboss.sh
bash install_sbwt.sh
bash install_sshash.sh
