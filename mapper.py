#!/usr/bin/python
import pycurl
import json
import sys
import StringIO

# download appropriate json file
def catalogSearch(filename):
	postData = '{"query": {"query_string" : {"fields":"filename","query": "' \
		+ filename + '"}, "range":{} }, "facets":{}}'
	c = pycurl.Curl()
	c.setopt(pycurl.URL, "http://ccicatalog.ci.uchicago.edu:6543/search")
	b = StringIO.StringIO()
	c.setopt(pycurl.WRITEFUNCTION, b.write)
	c.setopt(pycurl.POST, 1)
	c.setopt(pycurl.POSTFIELDS, postData)
	c.perform()
	result = json.loads(b.getvalue())
	filelocations = []
	for elem in result['hits']['hits']:
		filelocations.append(elem['_source']['filelocation'])
	return filelocations

# get logical filename argvc[1]
if (len(sys.argv) > 2):
	if (sys.argv[1] == "-filename"):
		filename = sys.argv[2]
else:
	filename = None;

# turn filename into filelocation using the catalog
if (filename != None):
	filelocations = catalogSearch(filename)
	if (filelocations != []):
		for i in range(0, len(filelocations)):
			print "[" + str(i) + "] " + filelocations[i]
