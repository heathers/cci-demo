#!/usr/bin/python
import pycurl
import json
import sys
import StringIO
import argparse
import random
import os
import paramiko
from contextlib import closing
from scpclient import Write

REMOTE_LOGIN='hstoller'
REMOTE_PWD='daiquiri0415'
REMOTE_SRC='/home/hstoller/ccifiles/'

# post file metadata in json
def catalogpost(postdata):	
	#postdata as {"owner":"...", "filename":"...","filelocation":"..."}
	c = pycurl.Curl()
	c.setopt(pycurl.URL, "http://ccicatalog.ci.uchicago.edu:6543/files")
	b = StringIO.StringIO()
	c.setopt(pycurl.WRITEFUNCTION, b.write)
	c.setopt(pycurl.POST, 1)
	c.setopt(pycurl.POSTFIELDS, postdata)
	c.perform()

# parse argument owner and filename
parser = argparse.ArgumentParser(description='Enter files into catalog.')
parser.add_argument('-workingdir',help='directory in which the files are stored')
parser.add_argument('-owner',help='fileowner')
parser.add_argument('-experiment',help='experiment')
args = parser.parse_args()

# scp set up
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# for each file in current directory
for filename in os.listdir(args.workingdir):
	# randomly select one to send to
	# gsiftp://gridftp.lcrc.anl.gov//home/hstoller
	# gsiftp://gs2.mcs.anl.gov//home/hstoller
	# gsiftp://gs1.mcs.anl.gov//home/hstoller
	rand = random.random()*3;
	if (rand < 1):
		loc = "gsiftp://gridftp.lcrc.anl.gov/"
		REMOTE_HOST = "fusion.lcrc.anl.gov"
	elif (rand < 2):
		loc = "gsiftp://gs2.mcs.anl.gov/"
		REMOTE_HOST = "login2.mcs.anl.gov"
	else:
		loc = "gsiftp://gs1.mcs.anl.gov/"
		REMOTE_HOST = "login1.mcs.anl.gov"
	# send file via scp
	"""print "sending "+filename
	ssh_client.connect(REMOTE_HOST,username=REMOTE_LOGIN,password=REMOTE_PWD)
	with closing(Write(ssh_client.get_transport(), REMOTE_SRC)) as scp:
		scp.send_file(args.workingdir+filename, True)	
	"""
	# enter in catalog with -owner
	print "cataloging "+filename
	data = ('{"owner":"'+args.owner+'","filename":"'+filename+'","filelocation":"'+loc+REMOTE_SRC+filename+'","experiment":"'+args.experiment+'"}')
	catalogpost(data)
