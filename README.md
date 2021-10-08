# whoIsWatcher.py


## Tool description
1- Python tool that queries 5 domains from the WHOIS API each 24 hours. 
2- Normalizes the JSON request and monitor if from the previous day, those domains were tampered or not
3- If a domain was tampered it will send an email to the associated email in the conf.yaml
Requirements: Docker service running in your system.

## To run it with docker
1- Download the source code into an empty directory <br>
2- cd to the directory where the Dockerrun is configured
3- Run the following command 
> docker build --no-cache -t whoiswatcher .
4- Go to Docker Desktop and execute the container called whoiswatcher and open the CLI

## TOOL ARCHITECTURE
1- Python tool that uses apscheduler from python to run a whois request each 24 hours
2- 
![arquitecture](/media/whoisWatcherDiagram.png "Diagram")
