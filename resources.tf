# Configure Google Cloud Project Data Source
data "google_project" "existing" {
  project_id = "gcpa-415907"
}

# Artifact Registry Repository (assuming it depends on the bucket)
resource "google_artifact_registry_repository" "docker_images" {
  project       = data.google_project.existing.project_id
  location      = "us-central1"
  repository_id = "amazon-seller-ai"
  description   = "amazon-seller-ai images"
  format        = "DOCKER"
}
