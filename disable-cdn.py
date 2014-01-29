#!/usr/bin/python

#NOTE: this requires pythoon 2.3 minumum

###
# To the extent possible under law, Red Hat, Inc. has dedicated all copyright to this software to the public domain worldwide, pursuant to the CC0 Public Domain Dedication. 
# This software is distributed without any warranty.  See <http://creativecommons.org/publicdomain/zero/1.0/>.
###


__author__ = "Felix Dewaleyne"
__credits__ = ["Felix Dewaleyne"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Felix Dewaleyne"
__email__ = "fdewaley@redhat.com"
__status__ = "dev"

import xmlrpclib, sys, getpass
#connection part
client = xmlrpclib.Server("https://rhn.redhat.com/rpc/api")
sys.stderr.write("enter your RHN login: ")
login = raw_input().strip()
password = getpass.getpass(prompt="enter your RHN Password: ")
sys.stderr.write("\n")
key = client.auth.login(login,password)
#remove the password from memory
del password
systems = client.system.listUserSystems(key)
print str(len(systems))+" systems found"
i = 0
for system in systems:
    i+=1
    details = client.system.getDetails(key,system['id'])
    if details['location_aware_download'] == True:
        details['location_aware_download'] = False
        client.system.setDetails(key,details)
        status = r"system %d of %d : CDN disabled for system %d" % (i,len(systems), system['id'] )
    else:
        status = r"system %d of %d : CDN already disabled for system %s" % (i, len(systems), system['id'])
    print status,
print "done"
client.auth.logout(key)

