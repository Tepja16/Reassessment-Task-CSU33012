#!/usr/bin/env python

import time

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

def preprocess_csv():

	try:
		data = open('commit_data.csv')
	except:
		print("ERROR: CSV file not found")

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

def show_year_charts(year, year_data):

	fig, axes = plt.subplots(2, len(year_data), figsize=(15, 5))	

	i = 0
	for month, data in year_data.items():

		date = months[month-1]
		labels = list(data.keys())
		additions = [commit_data["additions"] for author, commit_data in data.items()]
		deletions = [commit_data["deletions"] for author, commit_data in data.items()]
			
		print(year, date)
		print(f"\t authors: {labels}")
		print(f"\t additions: {additions}")
		print(f"\t deletions: {deletions}")

		axes[0][i].set_title(f"{date}")
		
		if len(additions) == 1 and additions[0] == 0:
			pass
		else:
			axes[0][i].pie(additions, shadow=True, startangle=90, autopct='%1.2f%%', radius=1.45)
			axes[0][i].legend(labels, loc="best")
		
		if len(deletions) == 1 and deletions[0] == 0:
			pass
		else:
			axes[1][i].pie(deletions, shadow=True, startangle=90, autopct='%1.2f%%', radius=1.45)
			axes[1][i].legend(labels, loc="best")

		i = i + 1
	print()

	fig.suptitle(f"Charts for the year {year} organised by additions (top) and deletions (bottom)")
	
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

	task = None
	for commit in data:
		if commit["year"] != current_year or commit == data[len(data)-1]:
	
			processed_year_data = process_year_data(year_data)
			
			if task != None:
				time.sleep(5)
				task.terminate()

			task = Process(target=show_year_charts, args=[current_year, processed_year_data])
			task.start()
			
			year_data = []
			current_year = commit["year"]
		else:
			year_data.append(commit)
		
if __name__ == "__main__":
	data = preprocess_csv()
	process_data(data)
