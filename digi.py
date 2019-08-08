import requests
import json
import getpass

email = raw_input('Email: ')
password = getpass.getpass()

api_base = 'https://storage.rcs-rds.ro'

s = requests.Session()

# get auth token

token = s.get(api_base + '/token', headers = {
    'X-Koofr-Email': email,
    'X-Koofr-Password': password
}).headers['X-Koofr-Token']

s.headers['Authorization'] = 'Token ' + token

# get mount (Digi Cloud, Dropbox...)

mounts = s.get(api_base + '/api/v2/mounts').json()['mounts']

mount = [x for x in mounts if x['name'] == 'Digi Cloud'][0]

print mount['name']

# list files

files = s.get(api_base + '/api/v2/mounts/' + mount['id'] + '/files/list', params = {'path': '/'}).json()['files']

for file in files:
    print file['name']

# get file

print s.get(api_base + '/content/api/v2/mounts/' + mount['id'] + '/files/get', params = {'path': '/test.txt'}).content

# upload file

print s.post(api_base + '/content/api/v2/mounts/' + mount['id'] + '/files/put', params = {'path': '/'}, files = {
    'file': ('filename.txt', 'file content')
}).json()[0]['name']

# create directory

s.post(api_base + '/api/v2/mounts/' + mount['id'] + '/files/folder', params = {'path': '/'},
    data = json.dumps({
        "name": "new directory"
    }),
    headers = {
        'content-type': 'application/json'
    }
)