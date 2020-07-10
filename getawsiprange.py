__author__ = "dyjang"

import requests
import config
import pprint

_URL = config.url
_REGION = config.region
_SERVICE = config.service


def load_aws_json():
    r = requests.get(_URL)
    return r.json()


def get_created_date(aws_dict):
    return aws_dict['createDate']


def get_filtered_pref_list(prefix_arr):
    filtered_arr = []
    for prefix in prefix_arr:
        if _REGION == prefix['region'] and _SERVICE == prefix['service']:
            filtered_arr.append(prefix)

    return filtered_arr


def get_filtered_acls_ip_list(filtered_arr):
    acls_arr = []
    for prefix in filtered_arr:
        acls = prefix['ip_prefix']
        acls_arr.append(acls)

    return set(acls_arr)


def get_filtered_acls_pref_ip_list(filtered_arr):
    acls_arr = []
    for prefix in filtered_arr:
        acls = prefix['ip_prefix'].split('.')[0]
        acls_arr.append(acls)

        # if acls == '150':
        #     print(f'{prefix}')

    return set(acls_arr)


def teams_webhook(msg):
    url = config.teams
    message = msg

    hd = {
        'Content-Type': 'application/json'
    }

    dt = message

    r = requests.post(url, headers=hd, json=dt)

    return r.status_code


def main():
    aws_dict = load_aws_json()
    print(f'[-] Get created date : {get_created_date(aws_dict)}')
    prefix_list = aws_dict['prefixes']

    filtered_list = get_filtered_pref_list(prefix_list)
    print(
        f'[-] Get count of searched by {_REGION} : {len(filtered_list)}')

    filtered_acls_ip_list = get_filtered_acls_ip_list(filtered_list)
    print(
        f'[-] Get count filtered A class IP prefix list : {len(filtered_acls_ip_list)}')
    print(
        f'[-] Get filtered IP prefix list : {filtered_acls_ip_list}')

    filtered_acls_pref_ip_list = get_filtered_acls_pref_ip_list(filtered_list)
    print(
        f'[-] Get filtered A class IP prefix list : {filtered_acls_pref_ip_list}')

    message = {
        "themeColor": "0076D7",
        "summary": "AWS IP Range Checker",
        "sections": [{
            "facts": [{
                "name": "Based URL",
                "value": _URL
            }, {
                "name": "Created Date",
                "value": get_created_date(aws_dict)
            }, {
                "name": "Filtered IP prefix list",
                "value": str(filtered_acls_ip_list)
            }, {
                "name": "Filtered A class IP prefix list",
                "value": str(filtered_acls_pref_ip_list)
            }]
        }]
    }
    res = teams_webhook(message)

    print(f'[-] Teams webhook result : {res}')


if __name__ == "__main__":
    main()
