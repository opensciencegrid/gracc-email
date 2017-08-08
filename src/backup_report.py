

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

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def parse_dir(remote_path, how_old=7):
    "Parse a single directory"
    context = gfal2.creat_context()
    to_return = {}
    to_return['total_size'] = 0
    to_return['total_files'] = 0
    to_return['old_total_size'] = 0
    to_return['old_total_files'] = 0
   
    st = context.stat(str(remote_path))
    if not stat.S_ISDIR(st.st_mode):
        raise Exception("Remote file %s is not a directory" % remote_path)
    
    directory = context.opendir(str(remote_path))
    st = None
    
    while True:
        (dirent, st) = directory.readpp()
        if dirent is None or dirent.d_name is None or len(dirent.d_name) == 0:
            break
        mtime = datetime.datetime.fromtimestamp(int(st.st_mtime))
        if mtime > (datetime.datetime.now() - datetime.timedelta(days=how_old)):
            to_return['total_size'] += st.st_size
            to_return['total_files'] += 1
        if mtime < (datetime.datetime.now() - datetime.timedelta(days=how_old)) and mtime > (datetime.datetime.now() - datetime.timedelta(days=how_old*2)):
            to_return['old_total_size'] += st.st_size
            to_return['old_total_files'] += 1
   
    return to_return


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
        results = parse_dir(directory)
        print "For directory %s: %s, %i files" % (directory, sizeof_fmt(results['total_size']), results['total_files'])
        print "Old: %s, %i" % (sizeof_fmt(results['old_total_size']), results['old_total_files'])


if __name__ == "__main__":
    main()


