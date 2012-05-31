#!/usr/bin/python
import pycurl
import json
import sys
import StringIO
import optparse
#import argparse

# download appropriate json file
def catalogSearch(field, fieldvalue):
	pagenum = 0;
	filelocations = []
	while True:
		postData = '{"query": {"query_string" : {"fields":"'+field+'","query": "' \
			+ fieldvalue + '"}, "range":{} }, "facets":{}, "hpages":"'+str(pagenum)+'"}'
		c = pycurl.Curl()
		c.setopt(pycurl.URL, "http://ccicatalog.ci.uchicago.edu:6543/search")
		b = StringIO.StringIO()
		c.setopt(pycurl.WRITEFUNCTION, b.write)
		c.setopt(pycurl.POST, 1)
		c.setopt(pycurl.POSTFIELDS, postData)
		c.perform()
		result = json.loads(b.getvalue())
		if (result['hits']['hits'] == []):
			break
		for elem in result['hits']['hits']:
			filelocations.append(elem['_source']['filelocation'])
		pagenum = pagenum+1
	return filelocations

# parse arguments filename and n
parser = optparse.OptionParser()
parser.add_option('-f',action='store',dest='field')
parser.add_option('-v',action='store',dest='fieldvalue')
parser.add_option('-n',action='store',dest='num',type="int")
options, args = parser.parse_args()
#parser = argparse.ArgumentParser(description='Map logical filename to physical filename using catalog.')
#parser.add_argument('-filename',help='logical filename for lookup') 
#parser.add_argument('-n',type=int,help='max number of files in result')
#args = parser.parse_args()

# turn filename into filelocation using the catalog
if (options.filename != None):
	filelocations = catalogSearch(options.filename)
	numlocations = options.num if len(filelocations) > options.num else len(filelocations)
	if (numlocations != 0):
		for i in range(0, numlocations):
			print "[" + str(i) + "] " + filelocations[i]
