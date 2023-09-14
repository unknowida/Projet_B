import requests
import json
import warnings

warnings.simplefilter('ignore', requests.packages.urllib3.exceptions.InsecureRequestWarning)

def test_servicea():
    # Endpoint, assuming it's the same as the form's action attribute
    url = 'https://localhost:8443/microa/' # Update this to the correct endpoint
    
    response = requests.get(url, verify=False)
    

    # Check for a successful post creation.
    # This might be a 200 OK, a redirect (302), or another status code, adjust the assertion accordingly.
    if response.status_code == 200:
        print("Code 200: Test réussi")
    else:
        print(f"Test échoué. Code: {response.status_code}")
        exit(1)

test_servicea()

def test_servicea_list_posts():
    # Endpoint, assuming it's the same as the form's action attribute
    url = 'https://localhost:8443/microa/list_posts' # Update this to the correct endpoint
    
    response = requests.get(url, verify=False)
    

    # Check for a successful post creation.
    # This might be a 200 OK, a redirect (302), or another status code, adjust the assertion accordingly.
    if response.status_code == 200:
        print("Code 200: Test réussi")
    else:
        print(f"Test échoué. Code: {response.status_code}")
        exit(1)

test_servicea_list_posts()

def test_serviceb():
    # Endpoint, assuming it's the same as the form's action attribute
    url = 'https://localhost:8443/microb/' # Update this to the correct endpoint
    
    response = requests.get(url, verify=False)
    

    # Check for a successful post creation.
    # This might be a 200 OK, a redirect (302), or another status code, adjust the assertion accordingly.
    if response.status_code == 200:
        print("Code 200: Test réussi")
    else:
        print(f"Test échoué. Code: {response.status_code}")
        exit(1)

test_serviceb()

def test_serviceb_list_posts():
    # Endpoint, assuming it's the same as the form's action attribute
    url = 'https://localhost:8443/microb/list_pages' # Update this to the correct endpoint
    
    response = requests.get(url, verify=False)
    

    # Check for a successful post creation.
    # This might be a 200 OK, a redirect (302), or another status code, adjust the assertion accordingly.
    if response.status_code == 200:
        print("Code 200: Test réussi")
    else:
        print(f"Test échoué. Code: {response.status_code}")
        exit(1)

test_servicea_list_posts()

def test_servicec():
    # Endpoint, assuming it's the same as the form's action attribute
    url = 'https://localhost:8443/microc/' # Update this to the correct endpoint
    
    response = requests.get(url, verify=False)
    

    # Check for a successful post creation.
    # This might be a 200 OK, a redirect (302), or another status code, adjust the assertion accordingly.
    if response.status_code == 200:
        print("Code 200: Test réussi")
    else:
        print(f"Test échoué. Code: {response.status_code}")
        exit(1)

test_servicec()