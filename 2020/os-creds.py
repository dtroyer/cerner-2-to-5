#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

# creds.py - Get OpenStack credentials from clouds.yaml if available

# Tools that do not recognize the clouds.yaml file supported by
# OpenStack SDK and OpenStackClient can still use the file to set
# environment variables.
# https://docs.openstack.org/python-openstackclient/latest/configuration/index.html

# Best used as an alias, due to a bug in bash 3.2 the invocation can not
# use simple process redirection, so on MacOS:
# source /dev/stdin <<< "$(os-creds.py)"

import os

try:
    import openstack
    from openstack.config import loader
except:
    print("openstacksdk not found")
    exit(1)

# List the attributes we care about for auth
attrs = ["identity_api_version"]
auth_attrs = ["auth_url", "domain_id", "domain_name", "password",
    "project_domain_id", "project_domain_name", "project_id",
    "project_name", "user_domain_id", "user_domain_name", "username"]

# Get the configuration from clouds.yaml
config = loader.OpenStackConfig(load_envvars=False)

CLOUD = os.getenv('OS_CLOUD', '')
if (CLOUD not in config.get_cloud_names()):
    print("cloud not found: %s" % CLOUD)
    exit(2)

cloud = config.get_one(CLOUD)
auth = cloud.get_auth_args()

for a in auth_attrs:
    if a in auth:
        print("%s=%s" % ("OS_" + a.upper(), auth[a]))

for a in attrs:
    if a in cloud.config:
        print("%s=%s" % ("OS_" + a.upper(), cloud.config[a]))

# cerner_2^5_2020
