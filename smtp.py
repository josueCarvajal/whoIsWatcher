import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def build_body_alert_email(cache_hash, current_hash, cache_file, current_file, domain_name):
    message = """
    Dear administrator,
    We have found an inconsistency between yesterday's files and today request's

    Domain name: {},
    
    Hash from yesterday: {},
    
    Hash from today: {},

    Original whois record: {},
    
    
    Tampered whois record: {},
    
    Best,
    whoIsWatcher.py
    """.format(domain_name, cache_hash, current_hash, cache_file, current_file)

    return message


def build_body_info_email(domain_name):
    message = """
    Dear administrator,
    
    Everything seems to be good between yesterday's files and today request's for domain {}

    Best,
    whoIsWatcher.py
    """.format(domain_name)
    return message


''' 
    0 - no issues
    1 - tampered file'''

def send_email(body_message, code, receipt, sender_password):
    #The mail addresses and password
    sender_address = 'whoiswatcher@gmail.com'
    sender_pass = sender_password
    receiver_address = receipt
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address

    if code == 0:
        message['Subject'] = '[Info] Everything looks good'
    else:
        message['Subject'] = '[Warning] Whois record has been tampered!!'

    #The body and the attachments for the mail
    message.attach(MIMEText(body_message, 'plain', 'utf-8'))

    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    #print('Mail Sent')