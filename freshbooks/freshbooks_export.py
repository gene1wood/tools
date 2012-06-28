'''
Created on Feb 29, 2012

@author: "Gene Wood" <gene_wood@cementhorizon.com>

Requires : pip install refreshbooks
           pip install requests
           pip install gitpython
'''

from refreshbooks import api
from lxml import objectify
import git
import time
import ConfigParser
import os
import sys

# This is a workaround to gitpython not working under cron
# http://stackoverflow.com/questions/4399617/python-os-getlogin-problem
import pwd
os.getlogin = lambda: pwd.getpwuid(os.getuid())[0]

INIFILE = 'freshbooks_export.ini'

def main():
    config = ConfigParser.RawConfigParser({'domain' : 'example.freshbooks.com', 
                                           'apitoken' : 'put your api token here'})
    if os.path.exists(INIFILE):
        config.read(INIFILE)
    else:
        sys.exit("unable to fine %s config file. aborting" % INIFILE)
    if config.has_section('General'):
        domain = config.get('General', 'domain')
        apitoken = config.get('General', 'apitoken')
    else:
        sys.exit('%s is missing the [General] section. aborting' % INIFILE)
    if domain == 'example.freshbooks.com' or apitoken == 'put your api token here':
        sys.exit('You must define "domain" and "apitoken" in the %s config file. aborting' % INIFILE)
    if not os.path.isdir('data'):
        os.mkdir('data')
    c = api.TokenClient(
        domain,
        apitoken,
        user_agent='freshbooks_export/1.0'
    )

    typelist = ['invoice',
                'client',
                'payment',
                'recurring',
                'item',
                'estimate']

    for typename in typelist:
        f = open('data/%ss.txt' % typename, 'w')
        f.write(process(getattr(c, typename), '%ss' % typename, typename))
        f.close()

    try:
        repo = git.Repo("data")
        assert repo.bare == False
    except git.exc.InvalidGitRepositoryError:
        repo = git.Repo.init("data")
        assert repo.bare == False
    repo.index.add(['%ss.txt' % typename for typename in typelist])
    if len(repo.heads) == 0:
        # this repo has no commits
        repo.index.commit("freshbooks_export detected a change. committing %s" % time.strftime('%Y-%m-%dT%H:%M:%S'))
    elif len(repo.head.commit.diff(None)) > 0:
        # something has changed in our working copy
        repo.index.commit("freshbooks_export detected a change. committing %s" % time.strftime('%Y-%m-%dT%H:%M:%S'))

def process(obj, childname, grandchildname):
    per_page = 100
    page = 1
    retval = ''
    while page:
        print "fetching page %s of %s" % (page, childname)
        response = obj.list(per_page = per_page, page = page)
        subresponses = getattr(response[childname], grandchildname)
        retval += objectify.dump(response)
        retval += '\n'
        print "exported %s records from %s" % (len(subresponses), childname)
        if len(subresponses) < per_page:
            page = False
        else:
            page += 1
    return retval

if __name__ == "__main__":
    result = main()
