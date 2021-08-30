#!/usr/bin/python3

"""
Author: Yehor Smoliakov <egorsmkv@gmail.com>
License: GNU
"""

import json
from fail2ban.client.csocket import CSocket


def error(reason):
    """
    A helper function to form an error response.

    :param reason: What happened wrong
    :return: Dict of the response
    """

    return {'error': True, 'reason': reason}


def send_command(command):
    """
    This function send a command to the Fail2ban socket server

    :param command: A command
    :return: Result or an error from the server
    """

    if not command:
        return error('empty command')

    socket_file = '/var/run/fail2ban/fail2ban.sock'

    try:
        # command to the socket and set timeout
        client = CSocket(socket_file, timeout=20)
        client.settimeout(20)

        # send the command
        ret = client.send(command)

        # there is an error
        if ret[0] != 0:
            return error('incorrect response code')

        return {'error': False, 'data': ret[1]}
    except Exception as e:
        return error('exception occurred: ' + str(e))


def extract_stats(data):
    """
    This function extracts needed data from "status" command.

    :param data: Response from the server
    :return: Needed data
    """

    n_data = {
        'currently_banned': 0,
        'total_banned': 0,
        'banned_ips': [],
    }

    for k, v in data:
        if k == 'Actions':
            for k2, v2 in v:
                if k2 == 'Currently banned':
                    n_data['currently_banned'] = v2

                if k2 == 'Total banned':
                    n_data['total_banned'] = v2

                if k2 == 'Banned IP list':
                    n_data['banned_ips'] = v2

    return n_data


if __name__ == '__main__':
    cmd = ['status', 'freeswitch']

    response = send_command(cmd)

    if response['error']:
        print(json.dumps(response))
    else:
        stats = extract_stats(response['data'])
        print(json.dumps(stats))
