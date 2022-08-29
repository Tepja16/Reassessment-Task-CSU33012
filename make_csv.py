#!/usr/bin/env python

import csv
import sys
from github import Github

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

if __name__ == "__main__":
	if len(sys.argv) > 1:
		api_token = sys.argv[1] 
	else:
		api_token = ""
		print("No API key detected, you may want to enter one as there are almost 4500 commits.")

	print("Download commencing, this will take some time.")
	g = Github(api_token)

	user = g.get_user("d3")
	repo = user.get_repo("d3") 

	make_csv(repo)
