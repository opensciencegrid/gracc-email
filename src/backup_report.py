

import gfal2
from tabulate import tabulate
import smtplib
from email.mime.text import MIMEText
import locale
import datetime
import json
import argparse
import stat
import toml

def parse_dir(remote_path):
    "Parse a single directory"
    context = gfal2.creat_context()
    
    file = "gsiftp://red-gridftp3.unl.edu/user/hcc/gracc_job_backups"
    st = context.stat(remote_path)
    print st
    if not stat.S_ISDIR(st.st_mode):
        raise Exception("Remote file %s is not a directory" % remote_path)
    
    directory = context.opendir(remote_path)
    st = None
    
    while True:
        (dirent, st) = directory.readpp()
        if dirent is None or dirent.d_name is None or len(dirent.d_name) == 0:
            break
        print dirent
        print dirent.d_name
        print st
    
    



def add_args(parser):
    """
    Add options to the command line argument
    """
    parser.add_argument('emails', metavar='email', type=str, nargs='+',
                   help='Email(s) to send report')
    parser.add_argument('--smtp', type=str, dest='smtp', help='SMTP server to use')
    parser.add_argument('-c', "--conf", type=str, dest='config', help="Configuration file to use", default="/etc/gracc-backup-report/backup-report.conf")
    pass


def main():

    before = datetime.datetime.now()

    # Parse the arguments to the script
    parser = argparse.ArgumentParser(description='Report the state of backups')
    add_args(parser)
    args = parser.parse_args()

    # Read in the toml to find the directories to read
    config = toml.load(args.config)
    if not "directories" in config:
        raise Exception("Directories are not listed in the config file %s" % args.config)
    
    for directory in config['directories']:
        parse_dir(directory)
    


if __name__ == "__main__":
    main()


