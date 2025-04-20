resource "google_compute_instance" "default" {
  name         = var.instance_name
  machine_type = var.machine_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = var.image
    }
  }

  network_interface {
    network = var.network
    access_config {}
  }

  metadata = {
    ssh-keys = "${var.ssh_user}:${file(var.public_ssh_key_path)}",
    VAR_1 = var.target_bucket,
    VAR_2 = "compare-my-biometrics_dw"    
  }

  connection {
        type        = "ssh"
        user        = var.ssh_user
        private_key = file(var.private_ssh_key_path)
        host        = google_compute_instance.default.network_interface[0].access_config[0].nat_ip
      }
      
  provisioner "file" {
        source      = "../setup_scripts/"
        destination = "/home/${var.ssh_user}"
      }

  provisioner "file" {
        source      = "./terraform.tfvars"
        destination = "/home/${var.ssh_user}/terraform.tfvars"
      }

  provisioner "file" {
        source      = "../airflow-gcp/dags/.env"
        destination = "/home/${var.ssh_user}/.env"
      }

  provisioner "file" {
        source      = "../airflow-gcp/dags/fitbit_tokens.json"
        destination = "/home/${var.ssh_user}/fitbit_tokens.json"
      }

  provisioner "file" {
        source      = "${var.credentials}"
        destination = "/home/${var.ssh_user}/google_credentials.json"
      }

  provisioner "remote-exec" {
        inline = [
          "chmod +x ./deploy_on_compute_vm.sh",
          "./deploy_on_compute_vm.sh"
          ]
      }
      
}