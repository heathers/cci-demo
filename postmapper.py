#!/usr/bin/python
import pycurl
import json
import os, sys
import StringIO

# post file metadata in json
def catalogpost(postdata):	#postdata as {"owner":"...", "filename":"...","filelocation":"..."}
	c = pycurl.Curl()
	c.setopt(pycurl.URL, "http://ccicatalog.ci.uchicago.edu:6543/files")
	b = StringIO.StringIO()
	c.setopt(pycurl.WRITEFUNCTION, b.write)
	c.setopt(pycurl.POST, 1)
	c.setopt(pycurl.POSTFIELDS, postdata)
	c.perform()
	printfilename();
#catalogpost(data)

# get filename, owner, and location
if (len(sys.argv) > 4):
	if (sys.argv[3] == "-filename"):
		filename = sys.argv[4]
	if (sys.argv[1] == "-owner"):
		owner = sys.argv[2]
else:
	filename = None;
	owner = None;
loc = os.getcwd()

def printfilename():
	print "$ " + filename

data = '{"owner":"'+owner+'","filename":"'+filename+'","filelocation":"'+loc+'"}'
catalogpost(data)

# turn filename into filelocation using the catalog
"""
if (filename != None):
	filelocations = catalogSearch(filename)
	if (filelocations != []):
		for i in range(0, len(filelocations)):
			print "[" + str(i) + "] " + filelocations[i]
"""
