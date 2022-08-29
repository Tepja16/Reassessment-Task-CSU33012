# Reassessment-Task-CSU33012

This is the Reassessment Task for CSU33012.

This project is written in python using the pyGithub wrapper for the Github API. The project also uses the matplotlib library to generate the pie charts.
There are also some more libraries that your system probably has installed by default such as csv, sys, time, multiprocessing.

When the program is run a window for each year is generated containing the pie charts for each month of commits (additions and deletions) on the repository. These windows automatically close after a short interval and display the next yearly data. If you want to slow down the closing of the windows just edit the time.sleep() functions parameter on line 153 of final_project.py (Or you could easily rip out the threading statements and replace them with a simple call to the show_year_charts(current_year, processed_year_data) function.)

DETAILS:
When the final_project.py python script is ran in the same directory as the commit_data.csv the program will 
  1.) (processes_csv) Open the csv file and transform it into a list of dictionaries whos keys are year, month, author, additions, deletions. 
  2.) (process_data) run through a loop where the monthly data is gathered into a list . Once a years worth of data has been processed the year_data is sent to the process_year_data function to transform it into a dictionary whos keys are the months and whos values are also dictionaries whos keys are authors and who's entries are the additions and deletions. Additions and deletions are add togather under the authors key and finally 
  3.) The processed_yearly data is sent to the show_year_charts function which displays the window containing the <= 12 pie charts for the years (additions on top, deletions on the bottom). 

IMPORTANT NOTES:

When running final_project.py there are two deletions charts that wont show in year 2015, this is because only one person commited those months and the commited no deletions, so I just passed them in the function as I could figure out how to NOT draw them.

proj2.py attempt to generate the yearly windows for the pie charts in an online fashion. Due to some rare time ordering anomalies occuring in 2016 onwards the program breaks around the 2016 - 2015 interval.

Due to the above error I decided to rewrite the the program. The final program consists of two programs: make_csv.py and final_project.py. The make_csv.py will (when given a Github API key) attept to download the commit data into a csv file. The csv file is needed by the final_project.py which processed and displays the windows. 

For convenience I have included the .csv file for the commits in the repository so just download it along with the final_project.py and run the latter in the same directory as the former.
