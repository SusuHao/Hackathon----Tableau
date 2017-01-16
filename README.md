# Hackathon----Tableau
Creating an interactive platform that stands in users’ point of view. The target audience : anyone who looking for room to rent.

Installation
1. Install Tableau 10.0
2. Install R, install packages “Rserve”
3. Install Python 2.7


Execution
1. In R software, execute following code :
	library(Rserve)
	Rserve(args = "--vanilla")

Start Tableau
1. Open Tableau, click onto “Bus-service-subzone” in data source, in Measure Tab, right click “Bus_Impact”, and change the working directory to correct directory where those files are placed.
2. Do the same thing for “CallPy (1)” in Measure tab.
3. Click on Dashboard ”Title Vizili”, change to “PRESENTATION MODE”.
 
* If you want to get update the data files (.pkl), execute GetData.py.
