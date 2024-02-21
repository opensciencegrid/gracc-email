import gfal2
from tabulate import tabulate
import smtplib
from email.mime.text import MIMEText
import argparse
import stat
import datetime
import json

def sizeof_fmt(num, suffix='B'):
	for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, 'Yi', suffix)

class Directory:
	path = ''
	size = 0
	old_size = 0
	percent_change = 0
	file_count = 0
	files = []

	def __init__(self, path):
		self.path = path
		self.parse()

	def to_array(self):
		return [self.path, sizeof_fmt(self.size), sizeof_fmt(self.old_size), self.percent_change]

	def parse(self):
		how_old = 7
		context = gfal2.creat_context()
		cred_cert = gfal2.cred_new("X509_CERT", "/hostcert.pem")
		cred_key = gfal2.cred_new("X509_KEY", "/hostkey.pem")
		gfal2.cred_set(context, self.path, cred_cert)
		gfal2.cred_set(context, self.path, cred_key)
		total_size = 0
		total_files = 0
		old_total_size = 0
		st = context.stat(str(self.path))
		if not stat.S_ISDIR(st.st_mode):
			raise Exception("Remote file %s is not a directory" % self.path)
	
		directory = context.opendir(str(self.path))
		st = None
		
		while True:
			(dirent, st) = directory.readpp()
			if dirent is None or dirent.d_name is None or len(dirent.d_name) == 0:
				break
			mtime = datetime.datetime.fromtimestamp(int(st.st_mtime))
			if mtime > (datetime.datetime.now() - datetime.timedelta(days=how_old)):
				total_size += st.st_size
				total_files += 1
				self.files.append({'filename': dirent.d_name, 'size': sizeof_fmt(st.st_size)})
			if mtime < (datetime.datetime.now() - datetime.timedelta(days=how_old)) and mtime > (datetime.datetime.now() - datetime.timedelta(days=how_old*2)):
				old_total_size += st.st_size
		self.size = total_size
		self.old_size = old_total_size
		self.file_count = total_files
		self.percent_change = (float(total_size - old_total_size) / max(old_total_size, 1)) * 100 

def add_args(parser):
	parser.add_argument('emails', metavar='email', type=str, nargs='+', help='Email(s) to send report')
	parser.add_argument('--smtp', type=str, dest='smtp', help='SMTP server to use')

def main():
	before = datetime.datetime.now() 
	parser = argparse.ArgumentParser(description='Report the state of backups')
	add_args(parser)
	args = parser.parse_args()
  
	output = []

	paths = ["gsiftp://fndca1.fnal.gov/pnfs/fs/usr/fermigrid/gratia/gracc-jobs-raw/", "gsiftp://fndca1.fnal.gov/pnfs/fs/usr/fermigrid/gratia/gracc-ps-raw/", 
  "gsiftp://fndca1.fnal.gov/pnfs/fs/usr/fermigrid/gratia/gracc-transfers-raw/", "gsiftp://fndca1.fnal.gov/pnfs/fs/usr/fermigrid/gratia/gracc-ps-itb-raw/" ]
	directories = list(map(lambda path: Directory(path), paths))
	directory_data = list(map(lambda directory: directory.to_array(), directories))
	output = "<html><h3>Directories</h3>"
	output += tabulate(tabular_data=directory_data, headers=["Directory", "Last Week", "Previous Week", "Change (%)"], tablefmt="html")
	
	total_backed_up = 0
	for directory in directories:
		output += "<br />"
		output += "<h3>%s</h3>" % directory.path
		output += tabulate(tabular_data=directory.files, headers="keys", tablefmt="html")

		total_backed_up += directory.size

	# Calculate and report the time it took to generate the email
	after = datetime.datetime.now()
	difference = after - before
	output += "<br />"
	output += "<p>Took %i seconds to generate email.</p>" % (difference.seconds)
	output += "</html>"

	subject = "GRACC Backups - %s bytes backed up last week" % sizeof_fmt(total_backed_up)
	email_body = output
	
	# Create the email
	msg = MIMEText("<pre style=\"font-size:small\">" + email_body + "</pre>", 'html')
	msg['Subject'] = subject
	from_address = "gracc-support@ops.osg-htc.org"
	msg['From'] = from_address
	smtp_config = json.load(open("smtp-config.json"))
	s = smtplib.SMTP_SSL(host=smtp_config['host'], port=smtp_config['port'])
	s.login(user=smtp_config['user'], password=smtp_config['password'])

	for email in args.emails:
		msg['To'] = email
		s.sendmail(from_address, [email], msg.as_string())

	s.quit()

if __name__ == "__main__":
	main()