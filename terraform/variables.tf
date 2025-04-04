variable "project" {
  description = "Unique Project Name"
  default     = "dtc-de-446723"
  type        = string
}

variable "credentials" {
  description = "My Credentials"
  default     = "~/.google/credentials/dtc-de-446723-477851964567.json"
  #ex: if you have a directory where this file is called keys with your service account json file
  #saved there as my-creds.json you could use default = "./keys/my-creds.json"
  type        = string
}

variable "region" {
  description = "Region"
  type        = string
}

variable "location" {
  description = "Project Location"
  default = "US"
  type        = string
}


variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
  type        = string
}

variable "gcs_bucket_name" {
  description = "Storage Bucket Name, must be unique"
  type        = string
}

variable "bq_dataset_name" {
  description = ""
  #Update the below to what you want your dataset to be called
  default = "fitbit_dataset"
  type        = string
}

# VPC Variables
variable "vpc_network_name" {
  type    = string
}

variable "firewall_name" {
  type = string
}


# Compute Variables
variable "instance_name" {
  description = "Compute Engine instance name"
  type        = string
}

variable "machine_type" {
  description = "machine type of the instance"
  type        = string
}

variable "zone" {
  description = "deployment zone"
  type        = string
}

variable "image" {
  description = "OS image"
  type        = string
}

variable "ssh_user" {
  description = "SSH config username"
  type        = string
}

variable "public_ssh_key_path" {
  description = "directory path to the PUBLIC SSH key file"
  type        = string
}

variable "private_ssh_key_path" {
  description = "directory path to the PRIVATE SSH key file"
  type        = string
}