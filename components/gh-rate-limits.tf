# resource "time_sleep" "wait_for_repo_data" {
#   depends_on = [data.github_repository.repos]

#   create_duration = "60s"
# }

# resource "time_sleep" "wait_for_branch_data" {
#   depends_on = [data.github_branch.existing_branches]

#   create_duration = "60s"
# }

# resource "time_sleep" "wait_for_rate_limit" {
#   create_duration = "60s"

#   triggers = {
#     always_run = "${timestamp()}"
#   }
# }