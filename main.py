from apscheduler.schedulers.blocking import BlockingScheduler
import configparser
from datetime import datetime
import ast
import fileinput
import hashlib
import logging
import os
import pathlib

import yaml
from whoisapi import *

import smtp as mail



# Global paths

working_dir = pathlib.Path(__file__).parent.resolve()
log_file = working_dir.joinpath('watcher.log')
domains_yaml = working_dir.joinpath('domains.yaml')
parsed_json = working_dir.joinpath('parsed.json')
conf_file = working_dir.joinpath('conf.yaml')

logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

# Configuration files


def load_conf(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


# Load config

conf = load_conf(conf_file)
RECEIPT = conf.get('EMAIL').get('RECEIPT')
API_KEY = conf.get('API').get('API_KEY')


''' Change the API key to yours,
This can be read from a script.conf property file'''

client = Client(api_key=str(API_KEY))


'''
@return a list of the domains based on a domains.yaml file
'''


def read_domain_list_from_yaml():
    yaml_file = open(str(domains_yaml))
    domains = yaml.load(yaml_file, Loader=yaml.FullLoader)
    return domains.get("domains")


def build_dictionary(response):
    name = str(response['domain_name'])
    if name == "buildarat.com" or name == "pionsecar.com" or name == "cryptotradexinvest.com":
        administrative_root = str(response['administrative_contact'])
        registrant_root = str(response['registrant'])
        technical_root = str(response['technical_contact'])
        contact_email = str(response['contact_email'])
        administrative_dict = ast.literal_eval(administrative_root.replace('\n', ''))
        registrant_dict = ast.literal_eval(registrant_root.replace('\n', ''))
        technical_dict = ast.literal_eval(technical_root.replace('\n', ''))

        dictionary = {
            "domain_record": {
                "whoisCreatedDate": str(response['created_date']),
                "whoisUpdatedDate": str(response['updated_date']),
                "whoisExpiresDate": str(response['expires_date']),
                "registrantName": str(response['registrar_name']),
                "domain_name": str(response['domain_name']),
                "emails:": {
                    "registrant": administrative_dict['email'],
                    "administrativeContact": registrant_dict['email'],
                    "technicalContact": technical_dict['email'],
                    "contactEmail": contact_email
                }
            }
        }
        return dictionary
    else:
        administrative_root = str(response['administrative_contact'])
        registrant_root = str(response['registrant'])
        technical_root = str(response['technical_contact'])
        contact_email = str(response['contact_email'])
        dictionary = {
            "domain_record": {
                "whoisCreatedDate": str(response['created_date']),
                "whoisUpdatedDate": str(response['updated_date']),
                "whoisExpiresDate": str(response['expires_date']),
                "registrantName": str(response['registrar_name']),
                "domain_name": str(response['domain_name']),
                "emails:": {
                    "registrant": registrant_root,
                    "administrativeContact": administrative_root,
                    "technicalContact": technical_root,
                    "contactEmail": contact_email
                }
            }
        }
        return dictionary


def normalizer(response):
    dictionary = build_dictionary(response)
    domain_name = dictionary.get('domain_record').get('domain_name')
    if check_cache():
        append_json_to_file(dictionary)
        logging.info('[INFO] Saving first results to a file.')
    else:
        logging.info('[INFO] Checking cache...')
        result = compare_results(dictionary, domain_name)
        if result == 1:
            logging.info('[INFO] Saving first result for this domain into disk')
            append_json_to_file(dictionary)


def check_cache():
    cache = os.path.getsize(str(parsed_json))
    if cache <= 0:
        return True
    else:
        return False


def compare_results(dictionary, domain_name):
    archived_cached_hash = calculate_json_hash_from_cache(domain_name)
    # if not found return 1
    if archived_cached_hash == 1:
        return 1

    current_hash = calculate_hash(dictionary)
    logging.info("[INFO] validating archived hash " + archived_cached_hash)
    logging.info("[INFO] validating current hash " + current_hash)
    if archived_cached_hash == current_hash:
        logging.info("[INFO] Values are the identical from cache... this is good.")
        message = mail.build_body_info_email()
        mail.send_email(message, 0, str(RECEIPT))
    else:
        logging.warning("[WARN] Data has been tampered!")
        archived_file = retrieve_archived_whois(domain_name)
        logging.warning("[WARN] Updating registers...")
        update_json_file(dictionary, domain_name)

        message = mail.build_body_alert_email(archived_cached_hash, current_hash, dictionary, archived_file,
                                              domain_name)
        logging.warning("[WARN] Sending alert via email...")
        mail.send_email(message, 1, str(RECEIPT))


def append_json_to_file(dictionary):
    with open(str(parsed_json), "a") as fp:
        fp.write(str(dictionary) + '\n')
        fp.close()


def update_json_file(new_dictionary, domain_name):
    json_file = fileinput.input(files=str(parsed_json), inplace=1)
    for line in json_file:
        if domain_name in line:
            line = new_dictionary
        print(line)
    json_file.close()


def calculate_json_hash_from_cache(domain_name):
    json_file = open(str(parsed_json))
    for x in json_file:
        if not x.strip() == '':
            file = ast.literal_eval(x.replace('\n', ''))
            root_element = file['domain_record']
            current_domain_name = root_element['domain_name']
            if current_domain_name == domain_name:
                json_file.close()
                return calculate_hash(file)
    # if not found return 1
    json_file.close()
    return 1


def retrieve_archived_whois(domain_name):
    json_file = open(str(parsed_json))
    for x in json_file:
        if not x.strip() == '':
            file = ast.literal_eval(x.replace('\n', ''))
            root_element = file['domain_record']
            current_domain_name = root_element['domain_name']
            if current_domain_name == domain_name:
                return file


def calculate_hash(file):
    hash_object = hashlib.sha256(str(file).encode())
    return hash_object.hexdigest()


def do_rpc():
    domains = read_domain_list_from_yaml()
    try:
        for domain in domains:
            # Work smart .data method already validates empty values for the whois record
            response = client.data(str(domain))
            normalizer(response)
    except ValueError:
        logging.error("[ERROR] Response was empty for " + domains)


if __name__ == '__main__':
    logging.debug("[DEBUG] doing first do_rpc")
    do_rpc()  # first execution requires call
    scheduler = BlockingScheduler()
    scheduler.add_job(do_rpc(), 'interval', hours=24)
    scheduler.start()
