variable "instance_name" {
  description = "Compute Engine instance"
  type        = string
}

variable "machine_type" {
  description = "machine type of the instance"
  type        = string
}

variable "zone" {
  description = "Deployed zone for the instance"
  type        = string
}

variable "image" {
  description = "OS image for the instance"
  type        = string
}

variable "network" {
  description = "VPC name to associate with the instance"
  type        = string
}

variable "ssh_user" {
  description = "SSH configuration username"
  type        = string
}

variable "public_ssh_key_path" {
  description = "The path to the public SSH key file"
  type        = string
}

variable "private_ssh_key_path" {
  description = "Path to the private SSH key file"
  type        = string
}

variable "target_bucket" {
  description = "Path to the public SSH key file"
  type        = string
}

variable "credentials" {
  description = "Path to the service accounts google_credentials.json"
  type        = string
}

variable "compute_disk_size_GB" {
  description = "Gigabytes available for the vm disk"
  type        = string
}