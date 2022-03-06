"""
description:
    Stop Aliyun instance to save your money
    
requirements:
    pip install alibabacloud_ecs20140526==2.1.0
    pip install python-dotenv retry

"""

# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
import sys
import retry
from dotenv import load_dotenv

from typing import List

from alibabacloud_ecs20140526.client import Client as Ecs20140526Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_ecs20140526 import models as ecs_20140526_models

import logging

# Creating and Configuring Logger

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename=os.path.basename(__file__) + ".log",
                    filemode="w",
                    format=Log_Format,
                    level=logging.DEBUG)

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stdout))


class Server:
    def __init__(self):
        self.client = Ecs20140526Client(open_api_models.Config(
            access_key_id=os.environ.get("ALIYUN_AK_ID"),
            access_key_secret=os.environ.get("ALIYUN_AK_SECRET"),
            endpoint=os.environ.get("ALIYUN_ENDPOINT"),
        ))
        self.instance_id = os.environ.get('ALIYUN_INSTANCE_ID')
        self.status()

    def start(self) -> None:
        status = self.status()
        if status == "Starting":
            print("instance is starting")
            return
        
        if status == "Running":
            print("instance is already running")
            return

        start_instance_request = ecs_20140526_models.StartInstanceRequest(
            instance_id=self.instance_id
        )
        self.client.start_instance(start_instance_request)

    def stop(self) -> None:
        status = self.status()
        if status == "Stopped":
            print("instance is already stopped")
            return
        
        if status == "Stopping":
            print("instance is stopping")
            return
        
        stop_instance_request = ecs_20140526_models.StopInstanceRequest(
            instance_id=self.instance_id, stopped_mode="StopCharging"
        )
        retry.api.retry_call(self.client.stop_instance, fargs=[stop_instance_request],
                             tries=5, delay=30, backoff=2)

    def reboot(self) -> None:
        reboot_instance_request = ecs_20140526_models.RebootInstanceRequest(
            instance_id=self.instance_id
        )
        self.client.reboot_instance(reboot_instance_request)

    def status(self) -> str:
        describe_instance_attribute_request = ecs_20140526_models.DescribeInstanceAttributeRequest(
            instance_id=self.instance_id
        )
        response = self.client.describe_instance_attribute(
            describe_instance_attribute_request)
        if len(response.body.public_ip_address.ip_address) > 0:
            self.public_ip_address = response.body.public_ip_address.ip_address[0]
        return response.body.status


if __name__ == '__main__':
    load_dotenv()
    server = Server()
    if len(sys.argv) == 1:
        print("Usage: "+__file__+" [start|stop|reboot|status]")
        sys.exit(1)

    action = sys.argv[1]
    if action == 'start':
        server.start()
    elif action == 'stop':
        server.stop()
    elif action == 'reboot':
        server.reboot()
    elif action == 'status':
        print("status of " + server.instance_id + ": " + server.status())
        if server.public_ip_address:
            print("public ip address: " + server.public_ip_address)
