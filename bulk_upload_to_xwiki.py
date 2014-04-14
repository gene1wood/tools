#!/usr/bin/env python
'''Upload a collection of Markdown files into xwiki

One way this tool can be used is to migrate content from Confluence to xwiki.
To do so :
# Export the Confluence space to a collection of html files : https://confluence.atlassian.com/display/DOC/Exporting+Confluence+Pages+and+Spaces+to+HTML
# Convert the html files to Markdown with pandoc
```
for file in *.html; do pandoc -f html -t markdown -o "`basename "$file" .html`.md" "$file"; done
```
# Load the files into xwiki with this tool

'''
import os
import requests
import requests.auth
import xml.etree.ElementTree
import tempfile
import pprint
import sys

username='Admin'
password='admin'
xwikiurl='http://example.com/xwiki'

def create_pages(filelist, username, password):
  output={}
  for i in filelist:
    if i.endswith(".md"):
      with open(i,'r') as f:
        name=os.path.splitext(i)[0]
        output[name]="starting"
        root = xml.etree.ElementTree.Element('{http://www.xwiki.org}page')
        title = xml.etree.ElementTree.SubElement(root, '{http://www.xwiki.org}title')
        title.text = name
        syntax = xml.etree.ElementTree.SubElement(root, '{http://www.xwiki.org}syntax')
        syntax.text = 'markdown/1.1'
        content = xml.etree.ElementTree.SubElement(root, '{http://www.xwiki.org}content')
        content.text = f.read().decode('utf8')
        tree = xml.etree.ElementTree.ElementTree(root)
        with tempfile.TemporaryFile() as xmlfile:
          tree.write(file_or_filename=xmlfile,
            encoding='UTF-8',
            xml_declaration=True,
            default_namespace='http://www.xwiki.org')
          xmlfile.seek(0)
          data = xmlfile.read()
          #print(data)

          r=requests.put('%s/rest/wikis/xwiki/spaces/Main/pages/%s' % (xwikiurl, name),
            auth=requests.auth.HTTPBasicAuth(username, password),
            data=data,
            headers={'Content-Type': 'application/xml'})
          output[name]=r.status_code
          print(r.status_code)
          pprint.pprint(dict(r.headers))
          print(r.text)
  return output

def delete_pages(filelist, username, password):
  output={}
  for i in filelist:
    if i.endswith(".md"):
      name=os.path.splitext(i)[0]
      output[name]="starting"
      r=requests.delete('%s/rest/wikis/xwiki/spaces/Main/pages/%s' % (xwikiurl, name),
        auth=requests.auth.HTTPBasicAuth(username, password))
      output[name]=r.status_code
      print(r.status_code)
      pprint.pprint(dict(r.headers))
      print(r.text)
  return output

filelist=os.listdir(os.getcwd())

if len(sys.argv) < 2:
  print "Usage : %s [create|delete]" % sys.argv[0]
  exit(1)
elif sys.argv[1] == 'create':
  output = create_pages(filelist, username, password)
elif sys.argv[1] == 'delete':
  output = delete_pages(filelist, username, password)
else:
  print "Usage : %s [create|delete]" % sys.argv[0]
  exit(1)
  
pprint.pprint(output)