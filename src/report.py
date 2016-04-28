#!/usr/bin/env python

import math
import argparse
import elasticsearch
from elasticsearch_dsl import Search, A
from tabulate import tabulate
import smtplib
from email.mime.text import MIMEText
import locale
import datetime


def GetCountRecords(client, from_date, to_date, query = None):
    """
    Get the number of records (documents) from a date range
    
    :param elasticsearch.client client: The elasticsearch client to use for the search 
    :param str from_date: The from date.  It can be lucene date math, such as 'now-1d' for yesterday
    :param str to_date: The to date.  Can also use lucene date math.
    :query str query: Query string to limit the documents searched.
    :return: The total documents
    """
    s = Search(using=client, index='gracc-osg-*') \
        .filter('range', **{'@timestamp': {'from': from_date, 'to': to_date}}) \
        .params(search_type="count")

    response = s.execute()
    return response.hits.total

def ReportNumRecords(es):
    """
    Report the total records in the collector in a readable table
    
    :param elasticsearch.client client: The elasticsearch client to use for the search
    :return: A tuple - (text_report str, num_todays_records int, num_yesterday_records int)
    
    """
    toReturn = ""
    
    # Calcualte the total records today
    today_records = GetCountRecords(es, "now-1d", "now")
    yesterday_records = GetCountRecords(es, "now-2d", "now-1d")
    delta = "%+.2f%%" % ((float(today_records-yesterday_records)/float(yesterday_records))*100)
    
    # Print the total 
    headers = ["Yesterday", "Today", "Delta"]
    toReturn += "Total records:\n"
    toReturn += tabulate([[yesterday_records, today_records, delta]], headers, tablefmt='grid')
    return (toReturn, today_records, yesterday_records)

def ReportPerProbe(es):
    """
    Report the per probe records and delta in a readable table
    
    """
    toReturn = ""
    
    # Create the search and aggreagations (A)
    s = Search(using=es, index='gracc-osg-*')
    a = A('terms', field='ProbeName', size=0)

    s.aggs.bucket('day_range', 'range', field='@timestamp',
        ranges = [
            {'from': 'now-1d', 'to': 'now'},
            {'from': 'now-2d', 'to': 'now-1d'}
        ]) \
        .bucket('probenames', a)
    
    # Probably don't need a filter since we have ranges above
    #s = s.filter('range', **{'@timestamp': {'from': 'now-4d', 'to': 'now'}})
    
    response = s.execute()
    
    # Extract the doc_count for each probe for each day
    table = {}
    int_day = 0
    for day in response.aggregations.day_range.buckets:
        for probe in day.probenames.buckets:
            if not probe.key in table:
                # Initialize the table with 0's
                table[probe.key] = [0]*len(response.aggregations.day_range.buckets)
            table[probe.key][int_day] = probe.doc_count
        int_day += 1
    
    # Format the data for the tabulate library
    data = []
    for (k,v) in table.items():
        tmp_data = []
        tmp_data.append(k)
        # Calculate the delta, be sure to correct the divide by zero error
        v.append("%+.2f%%" % ((float(v[1]-v[0])/float(v[0] if v[0] > 0 else 1))*100))
        tmp_data.extend(v)
        data.append(tmp_data)
    
    # Sort the data by probename
    data = sorted(data, key=lambda el: el[0])
    
    headers = ["ProbeName", "Yesterday Records", 'Today Records', 'Delta']
    toReturn +=  "Records by Probe:\n"
    toReturn += tabulate(data, headers=headers, tablefmt='grid')
    return toReturn

def add_args(parser):
    """
    Add options to the command line argument
    """
    parser.add_argument('emails', metavar='email', type=str, nargs='+',
                   help='Email(s) to send report')
    parser.add_argument('--smtp', type=str, dest='smtp', help='SMTP server to use')
    pass


def main():
    
    before = datetime.datetime.now()
    
    # Parse the arguments to the script
    parser = argparse.ArgumentParser(description='Report the local collector state to email')
    add_args(parser)
    args = parser.parse_args()
    
    es = elasticsearch.Elasticsearch(timeout=60)
    email_body = ""
    
    cluster = elasticsearch.client.ClusterClient(es)
    health = cluster.health()
    if health['status'] == "green":
        subject = "GRACC collector OK"
    else:
        subject = "GRACC collector status: %s" % health['status']
        # Prefix the email with the health status
        email_body += json.dumps(health, sort_keys = True, indent=4, separators=(',', ': '))
    
    # Report the total number of records
    (text_report, today_records, yesterday) = ReportNumRecords(es)
    email_body += text_report
    
    locale.setlocale(locale.LC_ALL, 'en_US')
    pretty_records = locale.format("%d", today_records, grouping=True)
    subject += " - %s Records processed today" % pretty_records
    
    # A divider
    email_body += "\n" + ("-" * 75) + "\n"

    # Report the per-probe information
    email_body += ReportPerProbe(es)
    
    # Calculate and report the time it took to generate the email
    after = datetime.datetime.now()
    difference = after - before
    email_body += "\n\n"
    email_body += "Took %i seconds to generate email." % (difference.seconds)
    
    # Create the email
    msg = MIMEText("<pre style=\"font-size:small\">" + email_body + "</pre>", 'html')
    msg['Subject'] = subject
    msg['From'] = "GRACC-Collector"
    s = smtplib.SMTP('localhost')
    
    for email in args.emails:
        msg['To'] = email
        s.sendmail("GRACC-Collector", [email], msg.as_string())
    
    s.quit()
    


if __name__ == "__main__":
    main()


