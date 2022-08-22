from github import Github

import matplotlib.pyplot as plt
import numpy as np

import time

#y = np.array([35, 25, 25, 15])
#mylabels = ["Apples", "Bananas", "Cherries", "Dates"]

#plt.pie(y, labels = mylabels, startangle = 90)
#plt.show() 

# First create a Github instance:

# using an access token
g = Github("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")

#g = Github()
user = g.get_user("d3")
repo = user.get_repo("d3") 



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
			



#			print(f"The current year is: {current_year}")
#			print(f"commit author: {commit.commit.author.name}")
#			print(f"commit committer: {commit.commit.committer.name}")

			#if
#			print(f"commit date: y: {commit.commit.author.date.year}, m: {commit.commit.author.date.month}")
	

def list_commits(repo):

	i = 0
	for commit in repo.get_commits():
		print(f"no : {i}")
		#print(f"commit sha: {commit.sha}")
		print(f"commit author: {commit.commit.author.name}")
		#print(f"commit committer: {commit.commit.committer.name}")
		print(f"commit date: y: {commit.commit.author.date.year}, m: {commit.commit.author.date.month}")
		print(f"commit code additions: {commit.stats.additions}")
		print(f"commit code deletions: {commit.stats.deletions}")
		#print(f"no {i}: {commit.commit.author.name}  on  {commit.commit.author.date}, additions: {commit.stats.additions}")
		print()
		i = i+1


get_chart(repo)







