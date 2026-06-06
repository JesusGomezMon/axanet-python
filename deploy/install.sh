#!/bin/bash
# Script de instalación para Amazon Linux 2 en EC2 t2.micro
set -euo pipefail

APP_DIR="/opt/axanet-python"
REPO_URL="${REPO_URL:-https://github.com/JesusGomezMon/axanet-python.git}"
BRANCH="${BRANCH:-main}"

echo "=== Instalando Axanet Python en EC2 ==="

sudo yum update -y
sudo yum install -y python3 python3-pip git

sudo mkdir -p "$APP_DIR"
sudo chown ec2-user:ec2-user "$APP_DIR"

if [ ! -d "$APP_DIR/.git" ]; then
    git clone -b "$BRANCH" "$REPO_URL" "$APP_DIR"
else
    cd "$APP_DIR" && git pull origin "$BRANCH"
fi

cd "$APP_DIR"
pip3 install --user -r requirements.txt

sudo cp deploy/axanet.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable axanet
sudo systemctl restart axanet

echo "=== Instalación completada ==="
echo "Accede en: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8080"
