import argparse
import pathlib
from wks_tools import is_valid_hostname

#{ [hostname [--compare hostname_b]] | filename | [ldap ou string | cllo] }

parser = argparse.ArgumentParser(prog='argtest', usage='main parser usage')
subparsers = parser.add_subparsers()
host_parser = subparsers.add_parser('host')
host_parser.add_argument('hostname')
host_parser.add_argument('--compare')
file_parser = subparsers.add_parser('filename')
file_parser.add_argument('filename', help='filename of newline-separated hosts to scan')
ldap_parser = subparsers.add_parser('')
ldap_parser.add_argument('ou_string')

host_args = host_parser.parse_args()

if is_valid_hostname(host_args.hostname):
    if host_args.compare:
        if host_args.hostname.lower() == host_args.compare.lower(): 
            print('hostname matches compare hostname!!! WTF!!!')
        else:
            if is_valid_hostname(host_args.compare):
                print('comparing {} to {}'.format(host_args.hostname, host_args.compare))
            else:
                print('compare host {} is invalid'.format(host_args.compare))
    else:
        print('scanning host {}'.format(host_args.hostname))
else:
    try:
        file_args = file_parser.parse_args()
        pathlib.Path(file_args.filename).resolve()
    except FileNotFoundError:
        ldap_args = ldap_parser.parse_args()
        if 'ou' in ldap_args.ou_string or 'cllo' in ldap_args.ou_string:
            print('calling with ldap string {}'.format(ldap_args.ou_string))
    else:
        print('scanning file {}'.format(file_args.filename))
