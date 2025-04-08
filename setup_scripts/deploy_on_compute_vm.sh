#!/bin/bash
sudo snap install docker
sudo groupadd -f docker
sudo usermod -aG docker $(whoami)

echo "Waiting for Docker socket to be available..."
while [ ! -S /var/run/docker.sock ]; do sleep 1; done

sudo chown root:docker /var/run/docker.sock
sudo chmod 660 /var/run/docker.sock

newgrp docker <<EOF
if [ ! -d "compare-my-biometrics" ]; then
  git clone --branch cloud-migration --single-branch --depth 1 https://github.com/MichaelSalata/compare-my-biometrics.git
fi  

cp -f ./terraform.tfvars ./compare-my-biometrics/terraform/terraform.tfvars
cp -f ./fitbit_tokens.json ./compare-my-biometrics/airflow-gcp/dags/fitbit_tokens.json
bash update_vm_env.sh

cd ./compare-my-biometrics/airflow-gcp
mkdir ./logs ./plugins ./config
DOCKER_BUILDKIT=1 docker compose build
docker compose up -d airflow-init && docker compose up
EOF