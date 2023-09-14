#!/bin/bash

if [ ! -f ./nginx/keys/localhost-key.pem ] || [ ! -f ./nginx/keys/localhost.pem ]; then
    echo "Generating key and cert..."
    openssl req -x509 -newkey rsa:4096 -keyout localhost-key.pem -out localhost.pem -days 365 -nodes -subj "/C=US/ST=SomeState/L=SomeCity/O=SomeOrganization/OU=SomeOrganizationalUnit/CN=localhost"
    mv localhost-key.pem localhost.pem ./nginx/keys/
else
    echo "The key and/or certificate in ./nginx/keys already exist!"
fi
