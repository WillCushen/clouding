#!/usr/bin/python
#
"""
# Sample YAML file
#
- hosts: localhost
  gather_facts: no
  tasks:
  - name: Disable DHCP on Out-Of-Band Management Controller
    oob_dhcp_set_false:
      leased_bmc_ip: 127.0.0.1
      fixed_bmc_ip: 10.10.10.10
      fixed_bmc_netmask: 10.10.10.10/24
      bmc_username: username
      bmc_password: password
    register: result

  - debug: var=result
#
# Return Values
#
# failed: one of True or False
# changed: False
# msg: "HTTP Response {{ result }}. DHCP on iLO {{ leased_bmc_ip }} has successfully been disabled. A reset is now required to update the changes."
#
"""
#
#
# Do NOT change below this line ...
# Setup parameters passed to ansible module.
#
def main():
  # The AnsibleModule provides lots of common code for handling returns, parses your arguments for you, and allows you to check inputs
  module = AnsibleModule(
    argument_spec=dict(
      leased_bmc_ip=dict(type='str', required=True),
      fixed_bmc_ip=dict(type='str', required=True),
      fixed_bmc_netmask=dict(type='str', required=True),
      bmc_username=dict(type='str', required=True),
      bmc_password=dict(type='str', required=True),

    ),
    supports_check_mode=False,
  )

  leased_bmc_ip = module.params['leased_bmc_ip']
  fixed_bmc_ip = module.params['fixed_bmc_ip']
  fixed_bmc_netmask = module.params['fixed_bmc_netmask']
  bmc_username = module.params['bmc_username']
  bmc_password = module.params['bmc_password']

#
# Remove warning messages if this is insecure
#
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

  url = 'https://%s/redfish/v1/Managers/1/EthernetInterfaces/1/' % leased_bmc_ip
  headers = {'content-type': 'application/json'}
  payload = {
        "IPv4Addresses": [{
               "Address": fixed_bmc_ip,
               "SubnetMask": fixed_bmc_netmask
        }],

        "Oem": {
               "Hpe": {
                       "DHCPv4": {
                              "Enabled": False
                       }
               }
        }
    }


  try:
        response=requests.patch(url, data=json.dumps(payload), headers=headers, verify=False, auth=(bmc_username,bmc_password), timeout=30)
        status=response.status_code
        module.exit_json(changed=False, status=status, fixed_bmc_ip=fixed_bmc_ip)
  except requests.exceptions.RequestException as e:
        module.fail_json(changed=False, msg="%s" % (e))

#
# Main body
#
from ansible.module_utils.basic import *
import requests
import json
import os
import urllib3

if __name__ == '__main__':
    main()
