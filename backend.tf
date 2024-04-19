terraform {
  backend "gcs" {
    bucket = "gcp-terraform-state-amazon-seller-ai"
    prefix = "terraform/state"
  }
}