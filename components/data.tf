data "github_team" "admin" {
  slug = "platform-operations" # Add more teams here if you want to exlcude them from the rulesets
}

data "local_file" "repos_json" {
  filename = "${path.module}./production-repos.json"
}