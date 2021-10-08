# whoIsWatcher.py


## Tool description
1- Python tool that queries 5 domains from the WHOIS API each 24 hours. <br>
2- Normalizes the JSON request and monitor if from the previous day, those domains were tampered or not <br>
3- If a domain was tampered it will send an email to the associated email in the conf.yaml <br>
4- Once a tampered domain was found it will update the parsed.json file with the latest data. <br>

# Pre-requisites: 
1- Docker service running in your system. <br>
2- Once downloaded modify the conf.yaml with your own whoisAPI key, put your own email and the **PASSWD for the sender will be emailed** :) <br> <br>
![conf](/media/conf.PNG "configuration file")

## To run it with docker
1- Download the source code into an empty directory <br> 
2- cd to the directory where the Dockerrun is configured <br>
3- Run the following command, it may take a little bit, there are 15 things to build :) <br>
> docker build --no-cache -t whoiswatcher . 
<br>
4- Go to Docker Desktop > Images > Click Run > Run
<br>

![docker_images](/media/imagesOnDisk.PNG "images")
<br>
5- And here you can open the console 
<br>

![console](/media/console.PNG "running instance") 
<br>
6- All the project files are saved under /opt/whois_watcher/, here is how it looks
<br>

![linux_box](/media/container_files.PNG "container files")
<br>
7- You can monitor the application logs with <br> <br>
> tail -F /opt/whois_watcher/
<br>

![logs](/media/logs.PNG "logs")
<br>

## How to test
1- By default, the first execution will validate with a pre-existing parsed.dict file. So you may only receive INFO emails saying that everything is OK. <br>
2- If you want to test the tampered functionality, follow the next steps: <br>

### Testing the tampered functionality
1- Before building your docker image, open the file called parsed.dict <br>
2- Modify the **value** of a key, for example change the hour and save <br>
3- Build your docker instance again <br>
4- In the first startup you will receive a warning email message like this: <br>
![warning_email](/media/tampered_email.PNG "email sample") 
<br>
5- CAVEAT!!! Once a tampered file was found, the code will update that specific record with the latest one. So take into consideration that while testing

## TOOL ARCHITECTURE
1- Python tool that uses apscheduler from python to run a whois request each 24 hours <br>
2- It reads the domains from the domains.yaml and do an RPC request to the API <br> 
3- Then that response is parsed based on the JSON request of each individual domain and we use dict to handle everything <br> <br>
![arquitecture](/media/whoisWatcherDiagram.png "Diagram")


## Improvements - To Be Done in the future
1- A flag to enable/disable receiving INFO email messages
2- Hash the pasword since right now it is in plain text in the code
3- Keep an audit file of history of each individual domain instead of overwritting with the latest
