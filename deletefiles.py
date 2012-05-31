import pycurl
import json
import StringIO
import argparse

# first get all resourceIDs matching a criterion
def filenameToIdSearch(field,value):
	pagenum = 0;
	ids = []
	while True:
		postData = '{"query": {"query_string" : {"fields":"'+field+'","query": "' \
			+ value + '"}, "range":{} }, "facets":{}, "hpages":"'+str(pagenum)+'"}'
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
			ids.append(elem['_id'])
		pagenum = pagenum+1
	return ids

# parse argument owner and filename
parser = argparse.ArgumentParser(description='Delete entries from catalog.')
parser.add_argument('-field',help='field to delete')
parser.add_argument('-value',help='value to delete')
args = parser.parse_args()

# then delete them all
def deleteIds(IDlist):
	for to_delete in IDlist:
		c = pycurl.Curl()
		c.setopt(pycurl.CUSTOMREQUEST, "DELETE")
		url = "http://ccicatalog.ci.uchicago.edu:6543/files/"+str(to_delete)
		c.setopt(pycurl.URL, url)
		c.perform()

ids = filenameToIdSearch(args.field, args.value)
print ids
deleteIds(ids)
