#!/bin/sh

###Script responsible for preparing environment to run app"
sudo pip install --upgrade pip

echo "installing dependencies"
sudo apt install python-bs4 
sudo pip install networkx
sudo pip install geojson
sudo pip install openpyxl
sudo pip install unidecode
