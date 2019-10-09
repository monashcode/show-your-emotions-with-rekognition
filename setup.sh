#!/bin/bash

set -e

sudo yum install npm -y
npm install -g c9
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --user
sudo python3 -m pip install -r requirements.txt

echo "==========> Dependencies installed successfully."
