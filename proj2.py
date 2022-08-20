from github import Github

# First create a Github instance:

# using an access token
g = Github("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")

#g = Github()
user = g.get_user("d3")
repo = user.get_repo("d3") 

#print(repo.get_commits())

i = 0
for commit in repo.get_commits():
	print(f"no {i}: {commit.commit.author.name}  on  {commit.commit.author.date}, additions: {commit.stats.additions}")
	i = i+1

#for stat in repo.get_stats_code_frequency():
#	print(f"week: {stat.week}, additions: {stat.additions}, deletions: {stat.deletions}")

