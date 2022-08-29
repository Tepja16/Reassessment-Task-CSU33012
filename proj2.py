from github import Github

import matplotlib.pyplot as plt

import time

import sys

from multiprocessing import Process


months = [
		"January",
		"February",
		"March",
		"April",
		"May",
		"June",
		"July",
		"August",
		"September",
		"October",
		"November",
		"December"
	]

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def parse_month_data(month_data):
	
	labels = [] 
	additions = []	
	deletions = []

	for key, val in month_data.items():

		labels.append(key)
		additions.append(val["additions"])
		deletions.append(val["deletions"])

	date = (
		month_data[labels[0]]["year"],
		months[month_data[labels[0]]["month"] - 1]
	)

	return date, labels, additions, deletions

def show_year_charts(year_data):

	fig, axes = plt.subplots(2, len(year_data), figsize=(15, 5))	

	i = 0
	for month_data in year_data:

		date, labels, additions, deletions = parse_month_data(month_data)

		print(date)
		print(f"\t authors: {labels}")
		print(f"\t additions: {additions}")
		print(f"\t deletions: {deletions}")

		year = date[0]
		month = date[1]
		axes[0][i].set_title(f"{date[1]}")
		
		axes[0][i].pie(additions, shadow=True, startangle=90, autopct='%1.2f%%', radius=1.45)
		axes[0][i].legend(labels, loc="best")
		axes[1][i].pie(deletions, shadow=True, startangle=90, autopct='%1.2f%%', radius=1.45)
		axes[1][i].legend(labels, loc="best")

		i = i + 1
	
	print()
	fig.suptitle(f"Charts for the year {date[0]} organised by additions (top) and deletions (bottom)")
	
	plt.show()
	
def get_chart(repo):

	# Set the initial year and month
	current_year = repo.get_commits()[0].commit.author.date.year
	current_month = repo.get_commits()[0].commit.author.date.month

	month_data = {}
	year_data = []

	i = 0
	l = repo.get_commits().totalCount

	task = None
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

			# Display the pie charts
			# Without killing the previous process a the screen will be (slowly) overwhelmed by windows of pie charts
			if task != None:
				task.terminate()
			

			# Display the charts, this is done is a seperate process as mthe atplotlib plt function pauses execution of the program 
			task = Process(target=show_year_charts, args=[year_data])

			task.start()

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

		printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
		i = i + 1
		
if __name__ == "__main__":
	if len(sys.argv) > 1:
		api_token = sys.argv[1] 
	else:
		api_token = ""

	g = Github(api_token)

	user = g.get_user("d3")
	repo = user.get_repo("d3") 

	get_chart(repo)
