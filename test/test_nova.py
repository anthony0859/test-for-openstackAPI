import os
import sys

reldir = os.path.join(os.path.dirname(__file__), '..')
absdir = os.path.abspath(reldir)
sys.path.append(absdir)

from keystone import keystone
from nova import nova

keystone_task = keystone.Keystone('114.212.189.132', '5000', '5000', '35357', 'admin', 'admin', 'ADMIN_PASS')
nova_task = nova.Nova(keystone_task)
print nova_task.create_server(name='server01', flavorRef='2', 
                            imageRef='0d192c86-1a92-4ac5-97da-f3d95f74e811', 
                            network_id='da002e34-57bb-492f-897b-6ed317b97cfc')
