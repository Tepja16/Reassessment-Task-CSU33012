# Reassessment-Task-CSU33012

This is the Reassessment Task for CSU33012.

This project is written in python using the pyGithub wrapper for the Github API. The project also uses the matplotlib library to generate the pie charts.
There are also some more libraries that your system probably has installed by default such as csv, sys, time, multiprocessing.

When the program is run a window for each year is generated containing the pie charts for each month of commits on the repository. These windows automatically close after a short interval and display the next yearly data. If you want to slow down the closing of the windows just edit the time.sleep() functions parameter on line 153 of final_project.py (Or you could easily rip out the threading statements and replace them with a simple call to the show_year_charts(current_year, processed_year_data) function.)

IMPORTANT NOTES:

proj2.py attempt to generate the yearly windows for the pie charts in an online fashion. Due to some rare time ordering anomalies occuring in 2016 onwards the program breaks around the 2016 - 2015 interval.

Due to the above error I decided to rewrite the the program. The final program consists of two programs: make_csv.py and final_project.py. The make_csv.py will (when given a Github API key) attept to download the commit data into a csv file. The csv file is needed by the final_project.py which processed and displays the windows. 

For convenience I have included the .csv file for the commits in the repository so just download it along with the final_project.py and run the latter in the same directory as the former.
