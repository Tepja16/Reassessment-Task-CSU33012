import csv 
import sys
import time

from github import Github

import matplotlib.pyplot as plt

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

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def make_csv(repo):

	year_csv = open('commit_data.csv', 'w')

	writer = csv.writer(year_csv)

	header = ['year', 'month', 'author', 'additions', 'deletions']
	writer.writerow(header)

	i = 0
	l = repo.get_commits().totalCount
	for commit in repo.get_commits():

		data = [
			commit.commit.author.date.year,
			commit.commit.author.date.month,
			commit.commit.author.name,
			commit.stats.additions,
			commit.stats.deletions
			]

		writer.writerow(data)

		printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
		i = i + 1

	year_csv.close()

def preprocess_csv():

	data = open('commit_data.csv')

	list_data = []
	for commit in data:
		list_data.append(commit.replace("\n", "").split(","))

	sorted_data = sorted(list_data, key=lambda x : x[0], reverse=True)[1:]

	processed_data = []
	for commit in sorted_data:
		processed_data.append({
			"year" : int(commit[0]),
			"month" : int(commit[1]),
			"author" : commit[2],
			"additions" : int(commit[3]),
			"deletions" : int(commit[4])
			})
	
	data.close()

	return processed_data

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

def process_year_data(year_data):
	
	processed_year_data = {}

	current_month = year_data[0]["month"]
	
	for commit in year_data:

		if commit["month"] not in processed_year_data:
			processed_year_data.update({
				commit["month"] : {
					commit["author"] : {
						"additions" : commit["additions"],
						"deletions" : commit["deletions"]
					}
				}
			})

		else:
			if commit["author"] in processed_year_data[commit["month"]]:
				processed_year_data[commit["month"]][commit["author"]]["additions"] = processed_year_data[commit["month"]][commit["author"]]["additions"] + commit["additions"]
				processed_year_data[commit["month"]][commit["author"]]["deletions"] = processed_year_data[commit["month"]][commit["author"]]["deletions"] + commit["deletions"] 
			else:
				processed_year_data[commit["month"]].update({
					commit["author"] : {
						"additions" : commit["additions"],
						"deletions" : commit["deletions"]
					}
				})


	return processed_year_data

def process_data(data):
	
	current_year = int(data[0]["year"])
	
	year_data = []
	for commit in data:
		if commit["year"] < current_year:
			
			processed_year_data = process_year_data(year_data)

			#print(processed_year_data )
			
			print(commit["year"])
			for key, val in processed_year_data.items():
				print(months[key-1], val)

			print()
			time.sleep(2)

			year_data = []
			current_year = commit["year"]
		else:
			year_data.append(commit)


		
if __name__ == "__main__":
	if len(sys.argv) > 1:
		api_token = sys.argv[1] 
	else:
		api_token = ""

	g = Github(api_token)

	user = g.get_user("d3")
	repo = user.get_repo("d3") 

	#make_csv(repo)

	data = preprocess_csv()

	process_data(data)

