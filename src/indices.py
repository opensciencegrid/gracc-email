#!/usr/bin/env python
import re
import tabulate

from elasticsearch import Elasticsearch


def gb(b):
    return b/1024.0/1024.0/1024.0

def kb(b):
    return b/1024.0


class IndicesReport(object):
    """
    Generates a report of total store size and number of documents
    for groups of indices defined by regex patterns.
    """
    def __init__(self, es_client, groups=[]):
        self.client = es_client
        self.groups = groups

        self.tab = []
        self.others = []

    def _addrow(self, name, num, size, docs):
        try:
            doc_size = float(size)/docs
        except ZeroDivisionError:
            doc_size = 0.0
        self.tab.append([
            name,
            num,
            "%0.1f"%gb(size),
            docs,
            "%0.1f"%kb(doc_size),
            ])

    def run(self):
        """
        Run queries to generate report. Called by report() if not already run.
        """
        r=self.client.indices.stats(metric='docs,store')
        idxs=r['indices'].keys()
        for group in self.groups:
            try:
                g = group['name']
                gre = group['regex']
            except KeyError:
                continue

            gidxs = filter(lambda i: re.match(gre,i),idxs)
            size = 0
            docs = 0
            for i in gidxs:
                size += r['indices'][i]['total']['store']['size_in_bytes']
                docs += r['indices'][i]['primaries']['docs']['count']
                idxs.remove(i)
            self._addrow(g,len(gidxs),size,docs)

        # ungrouped
        size = 0
        docs = 0
        for i in idxs:
            size += r['indices'][i]['total']['store']['size_in_bytes']
            docs += r['indices'][i]['primaries']['docs']['count']
            self.others.append(i)
        self._addrow('other',len(idxs),size,docs)

        # total
        size = r['_all']['total']['store']['size_in_bytes']
        docs = r['_all']['primaries']['docs']['count']
        self._addrow('**total**',len(r['indices']),size,docs)

    def report(self):
        """
        Returns report as string.
        """
        r = ''
        r += self.tabulate()
        r += '\n\nNOTE: Sizes include replicas.'
        r += '\n\nOther Indices\n'+('-'*80)+'\n'
        for i in sorted(self.others):
            r += str(i)+'\n'
        return r
                
    def tabulate(self, fmt="simple"):
        """
        Return report table as string. See tabulate docs for supported formats:
        https://pypi.python.org/pypi/tabulate
        """
        if len(self.tab) == 0:
            self.run()
        headers=["Index Group","# Indices","Size GB","# Docs","Size/Doc KB"]
        return tabulate.tabulate(self.tab, headers, tablefmt=fmt)
    

if __name__=='__main__':
    client = Elasticsearch()
    groups = [
            {'name':'GRACC (osg)', 'regex': r'gracc\.osg\.'},
            {'name':'GRACC (osg) [OLD]', 'regex': r'gracc-osg-[12]'},
            {'name':'GRACC (osg-transfer)', 'regex': r'gracc\.osg-transfer\.'},
            {'name':'GRACC (osg-itb)', 'regex': r'gracc\.osg-itb\.'},
            {'name':'OSG history', 'regex': r'osg-'},
            {'name':'LIGO history', 'regex': r'ligo-'},
            {'name':'Gratia Summary', 'regex': r'gratia-osg-summary'},
            {'name':'GRACC Monitor', 'regex': r'gracc-monitor'},
            {'name':'FIFE', 'regex':r'fife|logstash-fife'},
            {'name':'Marvel', 'regex': r'\.marvel'},
            {'name':'Kibana', 'regex': r'\.kibana'},    
            ]
    ir = IndicesReport(client,groups)
    print(ir.report())

