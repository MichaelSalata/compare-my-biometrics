variable "credentials" {
  description = "My Credentials"
  default     = "~/.google/credentials/dtc-de-446723-477851964567.json"
  #ex: if you have a directory where this file is called keys with your service account json file
  #saved there as my-creds.json you could use default = "./keys/my-creds.json"
}

variable "project" {
  description = "Unique Project Name"
  default     = "dtc-de-446723"
}

variable "region" {
  description = "Region"
  #Update the below to your desired region
  default = "us-central1"
}

variable "location" {
  description = "Project Location"
  #Update the below to your desired location
  default = "US"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}


variable "gcs_bucket_name" {
  description = "Storage Bucket Name, must be unique"
  #Update the below to a unique bucket name
  default = "dtc-de-446723-fitbit-bucket"
}
variable "bq_dataset_name" {
  description = ""
  #Update the below to what you want your dataset to be called
  default = "fitbit_dataset"
}
