#!/bin/bash
github_project_name="compare-my-biometrics"
github_repo_name="https://github.com/MichaelSalata/${github_project_name}.git"
git_branch="main"

sudo snap install docker
sudo groupadd -f docker
sudo usermod -aG docker $(whoami)

echo "Waiting for Docker socket to be available..."
while [ ! -S /var/run/docker.sock ]; do sleep 1; done

sudo chown root:docker /var/run/docker.sock
sudo chmod 660 /var/run/docker.sock

newgrp docker <<EOF
if [ ! -d "${github_project_name}" ]; then
  git clone --branch ${git_branch} ${github_repo_name}
fi

cp -f ./terraform.tfvars ./${github_project_name}/terraform/terraform.tfvars
cp -f ./fitbit_tokens.json ./${github_project_name}/airflow-gcp/dags/fitbit_tokens.json
cp -f ./.env ./${github_project_name}/airflow-gcp/dags/.env
bash update_vm_env.sh

cd ./${github_project_name}/airflow-gcp
mkdir ./logs ./plugins ./config
DOCKER_BUILDKIT=1 docker compose build
docker compose up -d airflow-init && docker compose up
EOF