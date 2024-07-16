data "github_organization" "org" {
  name = "hmcts-test"
}

data "local_file" "repos_json" {
  filename = "${path.module}./production-repos.json"
}