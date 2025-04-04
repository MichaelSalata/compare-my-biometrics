output "vpc_id" {
  value       = google_compute_network.vpc_network.id
  description = "VPC ID of created ."
}

output "firewall_id" {
  value       = google_compute_firewall.firewall.id
  description = "firewall rule ID ."
}
