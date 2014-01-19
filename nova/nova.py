import requests
import json

class Nova:
	def __init__(self, keystone):
		self.keystone=keystone
		self.public_urls = keystone.get_nova_public_urls()
		self.create_headers()
		self.amend_url(keystone.get_keystone_host())

	def amend_url(self, correct_host_name):
        	if not hasattr(self, 'public_urls'):
            		return
       		urls = []
        	for url in self.public_urls:
            		urls.append(url.replace('controller', correct_host_name))
            		self.public_urls = urls

	def create_headers(self):
        	token_id = self.keystone.get_token_id()
        	self.headers = {
            		"Content-type": "application/json",
            		"Accept": "application/json", 
            		'X-Auth-Token':token_id,
        	}

	def create_server(self, name, flavorRef, imageRef, network_id):
		public_url = self.public_urls[0]
		url = public_url + '/servers'
		print url

		server_info = {
		   'server':{
			'name' : name,
			'flavorRef' : public_url + '/flavors/' + flavorRef,
			'imageRef' : public_url + '/images/' + imageRef,
			'networks' : [
				{
					'uuid' : network_id
				}
			]
		   }	
		}		
		
		response = requests.post(url, data=json.dumps(server_info), headers=self.headers)
		status_code = response.status_code
		if status_code == 202:
			data = response.json()
			return data
		else:
			return None
