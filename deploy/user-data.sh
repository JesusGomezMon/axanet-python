#!/bin/bash
# User Data para EC2 - ejecuta al primer arranque de la instancia
set -euo pipefail

exec > /var/log/axanet-userdata.log 2>&1
echo "Inicio User Data: $(date)"

yum update -y
yum install -y python3 python3-pip git

APP_DIR="/opt/axanet-python"
mkdir -p "$APP_DIR"

# Clonar repositorio (actualizar URL con tu repo)
git clone -b main https://github.com/JesusGomezMon/axanet-python.git "$APP_DIR" || true

cd "$APP_DIR"
pip3 install -r requirements.txt

cp deploy/axanet.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable axanet
systemctl start axanet

echo "User Data completado: $(date)"
