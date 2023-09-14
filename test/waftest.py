import requests
import warnings

# Suppress only the single InsecureRequestWarning from requests
warnings.simplefilter('ignore', requests.packages.urllib3.exceptions.InsecureRequestWarning)

base_url = "https://localhost:8443/microa/"

headers = {
    "Content-Type": "application/json"
}

# 1. SQL Injection Test
response = requests.post(
    f"{base_url}/login",
    headers=headers,
    json={"username": "admin", "password": "password' OR '1' = '1'; -- "},
    verify=False  # Bypass SSL certificate verification
)
print("SQL Injection Test:", response.status_code)
if response.status_code != 403:
    print('Echec.'f'Code = {response.status_code}')
    exit(1)
else:
    print('Test réussi')
# 2. Cross-Site Scripting (XSS)
response = requests.get(
    f"{base_url}/search",
    headers=headers,
    params={"query": "<script>alert('xss');</script>"},
    verify=False
)
print("XSS Test:", response.status_code)
if response.status_code != 403:
    print('Echec.'f'Code = {response.status_code}')
    exit(1)
else:
    print('Test réussi')
# 3. Path Traversal
response = requests.get(
    f"{base_url}/files",
    headers=headers,
    params={"file": "../../../etc/passwd"},
    verify=False
)
print("Path Traversal Test:", response.status_code)
if response.status_code != 403:
    print('Echec.'f'Code = {response.status_code}')
    exit(1)
else:
    print('Test réussi')
# 4. Command Injection
response = requests.post(
    f"{base_url}/execute",
    headers=headers,
    json={"cmd": "ping; ls"},
    verify=False
)
print("Command Injection Test:", response.status_code)
if response.status_code != 403:
    print('Echec.'f'Code = {response.status_code}')
    exit(1)
else:
    print('Test réussi')
# 5. HTTP Request Smuggling
smuggling_headers = {
    "Transfer-Encoding": "chunked",
    "Content-Length": "4"
}
response = requests.post(
    f"{base_url}/endpoint",
    headers=smuggling_headers,
    data="5\r\nGPOST / HTTP/1.1\r\n...\r\n",
    verify=False
)
print("HTTP Request Smuggling Test:", response.status_code)
if response.status_code != 400:
    print('Echec.'f'Code = {response.status_code}')
    exit(1)
else:
    print('Test réussi')
# 6. User-Agent Impersonation
response = requests.get(
    f"{base_url}/endpoint",
    headers={"User-Agent": "SQLMap"},
    verify=False
)
print("User-Agent Impersonation Test:", response.status_code)
if response.status_code != 403:
    print('Echec.'f'Code = {response.status_code}')
    exit(1)
else:
    print('Test réussi')

