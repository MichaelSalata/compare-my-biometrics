#!/bin/bash
sudo snap install docker
sudo groupadd -f docker
# TODO pull the var.ssh_user from .tfvars instead of $(whoami)
sudo usermod -aG docker $(whoami)

echo "Waiting for Docker socket to be available..."
while [ ! -S /var/run/docker.sock ]; do sleep 1; done

sudo chown root:docker /var/run/docker.sock
sudo chmod 660 /var/run/docker.sock

newgrp docker <<EOF
if [ ! -d "compare-my-biometrics" ]; then
  # clone and update repo
  git clone https://github.com/MichaelSalata/compare-my-biometrics.git
fi  

cp ./terraform.tfvars ./compare-my-biometrics/terraform/terraform.tfvars
bash update_vm_env.sh


cd ./compare-my-biometrics/airflow-gcp
mkdir ./logs ./plugins ./config
DOCKER_BUILDKIT=1 docker compose build
docker compose up -d airflow-init && docker compose up
EOF