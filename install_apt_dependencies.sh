#!/bin/bash
set -euo pipefail

sudo apt update

# bifrost
sudo apt install -y build-essential cmake zlib1g-dev

# dynboss
sudo apt install -y libboost-all-dev libtclap-dev libsdsl-dev

# sbwt
sudo apt install -y g++ gcc cmake git python3-dev libz-dev

# sshash
sudo apt install -y zlib1g
