#!/usr/bin/python
#valid for python as provided on RHEL5 and 6

import xmlrpclib, sys, getpass

sys.stdout.write("RHN Login: ")
RHN_LOGIN = raw_input().strip()
RHN_PASSWORD = getpass.getpass(prompt="Password: ")

sys.stdout.write("Entitlement to add (default to sw_mgr_entitled) : ")
NEW_ENTITLEMENT = raw_input().strip()

#AFAIK those are the only two values acceptable
if NEW_ENTITLEMENT not in [ 'sw_mgr_entitled', 'enterprise_entitled']:
    sys.stderr.write("Value '%s' not in known list of accepted values, defaulting to 'sw_mgr_entitled' (update)\n" % (NEW_ENTITLEMENT))
    NEW_ENTITLEMENT = 'sw_mgr_entitled'

client = xmlrpclib.Server('http://xmlrp.rhn.redhat.com/rpc/api')
key = client.auth.login(RHN_LOGIN, RHN_PASSWORD)
#for security
del RHN_PASSWORD

for system in client.system.listUserSystems(key):
    try:
        client.system.upgradeEntitlement(key, system['id'], NEW_ENTITLEMENT)
        sys.stdout.write( "Updated system %s (ID-%d)\n" % (system['name'], system['id']) )
    except xmlrpclib.Fault, e:
        sys.stdout.write( "Unable to update system %s (ID-%d)\n" % (system['name'], system['id']) )
        sys.stderr.write(e)
        sys.stderr.write("\n")
        pass

client.auth.logout(key)

