data "github_team" "admin" {
  slug = "test"
}

data "local_file" "repos_json" {
  filename = "${path.module}./production-repos.json"
}
