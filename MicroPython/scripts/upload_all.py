import argparse
import json
import os
import time

from cloud_credentials import set_credentials
from common.cloud_providers import Providers
from generate_terraform import save_terraform_output_as_file
from upload_micropython import erase_chip, flash_micropython
from upload_scripts import flash_scripts

TERRAFORM_OUTPUT_PATH = "src/aws_config.json"
KAA_CONFIG_PATH = 'src/kaa_config.json'
THINGSBOARD_CONFIG_PATH = 'src/thingsboard_config.json'
CONFIG_OUTPUT_PATH = "src/config.json"


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', metavar='PORT', type=str, required=True,
                        help="Com port of the device")
    parser.add_argument('-c', '--cloud', metavar='CLOUD', type=str, required=True,
                        help="Cloud provider for IoT Starter: {}".format(
                            Providers.print_providers()))
    parser.add_argument('-s', '--sensor', metavar='SENSOR', type=str, required=False,
                        help="Sensor type in use (defaults to DHT22)")

    args = vars(parser.parse_args())
    return args


def save_additional_arguments(cloud_provider, sensor_type):
    """
    Save additional arguments (cloud provider and sensor in use)
    This script cannot access config file so it needs to create config file in advance
    """
    if sensor_type == None:
        sensor_type = "DHT22"
    
    cfg = {'cloud_provider': cloud_provider, 'sensor_type': sensor_type}
    with open(CONFIG_OUTPUT_PATH, 'w') as outfile:
        json.dump(cfg, outfile)


if __name__ == '__main__':
    args = parse_arguments()

    if args['cloud'] == Providers.AWS:
        if not os.path.isfile(TERRAFORM_OUTPUT_PATH):
            print("Generating terraform output..")
            save_terraform_output_as_file(TERRAFORM_OUTPUT_PATH)
        cloud_config_file_path = TERRAFORM_OUTPUT_PATH
    elif args['cloud'] == Providers.KAA:
        cloud_config_file_path = KAA_CONFIG_PATH
        set_credentials(args['cloud'])
    elif args['cloud'] == Providers.THINGSBOARD:
        cloud_config_file_path = THINGSBOARD_CONFIG_PATH
        set_credentials(args['cloud'])
    else:
        raise Exception("Wrong cloud provider! Only: {} are valid".format(
            Providers.print_providers()))
    
    save_additional_arguments(args['cloud'], args['sensor'])
    erase_chip(args['port'])
    flash_micropython(args['port'])
    time.sleep(4)
    flash_scripts(args['port'], cloud_config_file_path)
