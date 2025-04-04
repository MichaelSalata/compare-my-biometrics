output "instance_id" {
  value       = google_compute_instance.default.id
  description = "Compute Engine instance ID"
}

output "instance_public_ip" {
  value       = google_compute_instance.default.network_interface[0].access_config[0].nat_ip
  description = "public IP address of the Compute Engine instance."
}
