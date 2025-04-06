#!/bin/bash
# sudo snap install docker
sudo groupadd -f docker
sudo usermod -aG docker $(whoami)

sudo chown root:docker /var/run/docker.sock
sudo chmod 660 /var/run/docker.sock
newgrp docker <<EOF
if [ ! -d "compare-my-biometrics" ]; then
  echo "Cloning repo..."
  git clone https://github.com/MichaelSalata/compare-my-biometrics.git
else
  echo "Repo already cloned."
fi
cd ./compare-my-biometrics/airflow-gcp && mkdir ./logs ./plugins ./config
# sudo chown -R :docker ./dags ./logs ./plugins ./config ./example_data
# sudo chmod -R 775 ./dags ./logs ./plugins ./config ./example_data
docker compose up -d airflow-init && docker compose up
EOF