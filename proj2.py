from github import Github

import matplotlib.pyplot as plt
import numpy as np

import time

import sys

def show_chart(date, labels, data):
	plt.title(f"Additions made during the peroid of year: {date[0]}, month: {date[1]}")
	plt.pie(data, labels = labels, startangle = 90, autopct='%.0f%%')
	plt.show()


def get_chart(repo):

	current_year = repo.get_commits()[0].commit.author.date.year
	current_month = repo.get_commits()[0].commit.author.date.month

	month_data = {}
	for commit in repo.get_commits():
		

		if commit.commit.author.date.year != current_year:
			current_year = commit.commit.author.date.year
	
		if commit.commit.author.date.month != current_month:
			print(f"current_data: {month_data}")
			print(list(month_data.values()))
			print([i[0] for i in list(month_data.values())])
			print(list(month_data.keys()))
			
			show_chart(
				(current_year, current_month),
				list(month_data.keys()), 
				[i[0] for i in list(month_data.values())]
			)
			
			
			current_month = commit.commit.author.date.month 
			month_data = {}
			#time.sleep(1)
			
			




		if commit.commit.author.name not in month_data:
			month_data.update({
				commit.commit.author.name : [
					commit.stats.additions,
					commit.stats.deletions,
					commit.commit.author.date.year,
					commit.commit.author.date.month
				]
			})
		else:
			month_data[commit.commit.author.name][0] = month_data[commit.commit.author.name][0] + commit.stats.additions
			month_data[commit.commit.author.name][1] = month_data[commit.commit.author.name][1] + commit.stats.deletions
			
if __name__ == "__main__":

	if len(sys.argv) > 1:
		api_token = sys.argv[1] 
	else:
		api_token = ""


	g = Github(api_token)

	user = g.get_user("d3")
	repo = user.get_repo("d3") 

	get_chart(repo)
	

