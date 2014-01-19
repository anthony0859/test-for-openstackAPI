import requests
import json

class Keystone:
    def __init__(self, keystone_host, public_port, internal_port, 
                admin_port, tenant_name, username, password):
        self.set_keystone_endpoint(keystone_host, public_port, 
                                    internal_port, admin_port)
        self.set_user(tenant_name, username, password)
        if self.authenticate():
            self.create_headers()
            self.request_tenant_id()

    def set_keystone_endpoint(self, keystone_host, public_port,
                             internal_port, admin_port):
        self.keystone_host = keystone_host
        self.public_port = public_port
        self.internal_port = internal_port
        self.admin_port = admin_port

    def set_user(self, tenant_name, username, password):
        self.tenant_name = tenant_name
        self.username = username
        self.password = password

    def authenticate(self):
        url = 'http://' + self.keystone_host + ':' \
                + self.public_port + '/v2.0/tokens'
        user_info ={
            "auth": {
                "tenantName":self.tenant_name, 
                "passwordCredentials": {
                    "username": self.username,
                    "password": self.password
                },
            },
        }
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json"
        }
        response = requests.post(url, data=json.dumps(user_info), 
                                headers=headers)
        self.auth_status_code = response.status_code
        if self.auth_status_code == 200:
            self.auth_data = response.json()
            self.parse_auth_data(self.auth_data)
            return True
        else:
            """deal with faults"""
            print 'Authentication failed.'
            return False

    def create_headers(self):
        self.headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'X-Auth-Token':self.token_id,
        }

    def request_tenant_id(self):
        url = 'http://' + self.keystone_host + ':'+ self.admin_port \
                + '/v2.0/tenants?name=' + self.tenant_name
        response = requests.get(url, headers=self.headers)
        self.request_tenant_id_status = response.status_code
        if self.request_tenant_id_status == 200:
            self.tenant_data = response.json()
            self.parse_tenant_data(self.tenant_data)
            return True
        else:
            print 'Request Tenant ID Failed.'
            return False

    def parse_auth_data(self, auth_data):
        try:
            self.token_id = str(self.auth_data['access']['token']['id'])
            service_catalog_list = self.auth_data['access']['serviceCatalog']
        except KeyError as e:
            print 'KeyError:', e
            self.token_id = None
            service_caralog_list = None
        self.nova_public_urls = []
        self.neutron_public_urls = []
        for service in service_catalog_list:
            try:
                if service['name'] == 'nova':
                    for endpoint in service['endpoints']:
                        self.nova_public_urls.append(endpoint['publicURL'])
                if service['name'] == 'neutron':
                    for endpoint in service['endpoints']:
                        self.neutron_public_urls.append(endpoint['publicURL'])
            except KeyError:
                self.nova_public_urls = None
                self.neutron_public_urls = None

    def parse_tenant_data(self, tenant_data):
        self.tenant_id = self.tenant_data['tenant']['id']

    def is_authenticated(self):
        try:
            return self.auth_status_code == 200
        except AttributeError:
            return False

    def request_tenant_id_success(self):
        try:
            return self.request_tenant_id_status == 200
        except AttributeError:
            return False

    def get_token_id(self):
        if not self.is_authenticated():
            return None
        else:
            return self.token_id

    def get_nova_public_urls(self):
        if not self.is_authenticated():
            return None
        else:
            return self.nova_public_urls

    def get_neutron_public_urls(self):
        if not self.is_authenticated():
            return None
        else:
            return self.neutron_public_urls

    def get_keystone_host(self):
        return self.keystone_host

    def get_tenant_id(self):
        if not self.is_authenticated():
            return None
        if self.request_tenant_id_success():
            try:
                return self.tenant_id
            except AttributeError:
                return None
        else:
            return None
