from github import Github

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np

import time

import sys


def parse_month_data(month_data):
	
	labels = [] 
	data = []	

	for key, val in month_data.items():
		#date = (val["year"], val["month"])
		labels.append(key)
		data.append(val["additions"])

	date = (
		month_data[labels[0]]["year"],
		month_data[labels[0]]["month"]
	)

	return date, labels, data


def show_year_charts(year_data):
	#fig, axes = plt.subplots(1,len(year_data), figsize=(5, 5))

	#i = 0
	for month_data in year_data:

		date, labels, data = parse_month_data(month_data)

		print(date, labels, data)
		#axes[i].title(f"Additions made during the peroid of year: {date[0]}, month: {date[1]}")
		#axes[i].pie(data, labels = labels, startangle = 90, autopct='%.0f%%')

		#i = i + 1
	
	print()
	#plt.show()




def show_chart(date, labels, data):
	plt.title(f"Additions made during the peroid of year: {date[0]}, month: {date[1]}")
	
		
	plt.pie(data, labels = labels, startangle = 90, autopct='%.0f%%')
	plt.show()




def get_chart(repo):

	# Set the initial year and month
	current_year = repo.get_commits()[0].commit.author.date.year
	current_month = repo.get_commits()[0].commit.author.date.month

	month_data = {}
	year_data = []
	for commit in repo.get_commits():
		
		# Make a new month_data dictionary
		if current_month != commit.commit.author.date.month or (current_month == commit.commit.author.date.month and current_year != commit.commit.author.date.year):
			
			# Append the current month_data to the year data list			
			year_data.append(month_data)
			
			# Update the month index and empty the current month_data dictionary to prepare making a new month_data dictionary
			current_month = commit.commit.author.date.month 
			month_data = {}

		# Make a new year_data list
		if current_year != commit.commit.author.date.year:

			show_year_charts(year_data)
			# Update the year index and empty the current year_data list to prepare making a new year_data list
			current_year = commit.commit.author.date.year
			year_data = []
	

		# Append new month commit data to the year_data list
		if commit.commit.author.name not in month_data:

			# Append the commit data to the month_data list, the data is of the form {<author> : {"additions" : <additions>, "deletions" : <deletions>, "year" : <year>, "month" : <month>}}
			month_data.update({
				commit.commit.author.name : {
					"additions" : commit.stats.additions,
					"deletions" : commit.stats.deletions,
					"year" : commit.commit.author.date.year,
					"month" : commit.commit.author.date.month
				}
			})
		else:

			# If the authors name is already in the month_data dictionary for this month, add their additions and deletions together
			month_data[commit.commit.author.name]["additions"] = month_data[commit.commit.author.name]["additions"] + commit.stats.additions
			month_data[commit.commit.author.name]["deletions"] = month_data[commit.commit.author.name]["deletions"] + commit.stats.deletions
			
if __name__ == "__main__":

	# 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
	if len(sys.argv) > 1:
		api_token = sys.argv[1] 
	else:
		api_token = ""


	g = Github(api_token)

	user = g.get_user("d3")
	repo = user.get_repo("d3") 

	get_chart(repo)
	

