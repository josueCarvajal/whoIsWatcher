# whoIsWatcher.py


## Tool description
1- Python tool that queries 5 domains from the WHOIS API each 24 hours. 
2- Normalizes the JSON request and monitor if from the previous day, those domains were tampered or not
3- If a domain was tampered it will send an email to the associated email in the conf.yaml
4- Once a tampered domain was found it will update the parsed.json file with the latest data.

#Requirements: 
1- Docker service running in your system.
2- Once downloaded modify the conf.yaml with your own whoisAPI key, put your own email and ask me for the email SMTP password


## To run it with docker
1- Download the source code into an empty directory <br>
2- cd to the directory where the Dockerrun is configured
3- Run the following command, it may take a little bit, there are 15 things to build :)
> docker build --no-cache -t whoiswatcher . 
<br>
4- Go to Docker Desktop > Images > Click Run > Run 
5- And here you can open the console

and execute the container called whoiswatcher and open the CLI

## Configuration files:
1- There is a file called config.yaml that you can add your own email to receive the alerts and your own API key

## How to test
1-

cd /opt/whois_watcher

## TOOL ARCHITECTURE
1- Python tool that uses apscheduler from python to run a whois request each 24 hours
2- It reads the domains from the domains.yaml and do an RPC request to the API
3- Then that response is parsed based on the JSON request of each individual 
![arquitecture](/media/whoisWatcherDiagram.png "Diagram")
