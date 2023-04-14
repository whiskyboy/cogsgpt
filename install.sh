#!/bin/bash

# Install dependencies
sudo apt-get update
sudo apt-get install build-essential libssl-dev ca-certificates libasound2 wget

# Install python requirements
pip install -r requirements.txt

# activate env
source .env