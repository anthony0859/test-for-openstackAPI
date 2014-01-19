import os
import sys

reldir = os.path.join(os.path.dirname(__file__), '..')
absdir = os.path.abspath(reldir)
sys.path.append(absdir)

from keystone import keystone

keystone_task = keystone.Keystone('114.212.189.132', '5000', '5000', 
                                '35357', 'admin', 'admin', 'ADMIN_PASS')

print keystone_task.get_token_id()
print keystone_task.get_nova_public_urls()
print keystone_task.get_neutron_public_urls()
print keystone_task.get_tenant_id()


