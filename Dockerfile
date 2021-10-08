FROM python:3

RUN pip install whois-api

RUN pip install pyyaml

RUN pip install apscheduler

RUN mkdir /opt/whois_watcher

ADD domains.yaml /opt/whois_watcher/

ADD main.py /opt/whois_watcher/

ADD parsed.json /opt/whois_watcher/

ADD smtp.py /opt/whois_watcher/

ADD watcher.log /opt/whois_watcher/

ADD conf.yaml /opt/whois_watcher/


CMD ["python", "/opt/whois_watcher/main.py"]