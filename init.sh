#!/bin/bash

echo --------------------
echo Installing virtualenv
echo --------------------
sudo pip install virtualenv

echo --------------------
echo Installing Python 3.7.1 dependencies
echo --------------------
sudo apt-get update -y
sudo apt-get install -y build-essential
sudo apt-get install -y checkinstall
sudo apt-get install -y libreadline-gplv2-dev
sudo apt-get install -y libncursesw5-dev
sudo apt-get install -y libssl-dev
sudo apt-get install -y libsqlite3-dev
sudo apt-get install -y tk-dev
sudo apt-get install -y libgdbm-dev
sudo apt-get install -y libc6-dev
sudo apt-get install -y libbz2-dev
sudo apt-get install -y zlib1g-dev
sudo apt-get install -y openssl
sudo apt-get install -y libffi-dev
sudo apt-get install -y python3-dev
sudo apt-get install -y python3-setuptools
sudo apt-get install -y wget

echo --------------------
echo Prepare to build
echo --------------------
mkdir /tmp/Python37
cd /tmp/Python37

echo --------------------
echo Pull down Python 3.7.1, build, and install
echo --------------------
wget https://www.python.org/ftp/python/3.7.1/Python-3.7.1.tar.xz
tar xvf Python-3.7.1.tar.xz
cd /tmp/Python37/Python-3.7.1
./configure --enable-loadable-sqlite-extensions && sudo make && sudo make install

echo --------------------
echo Changing directories to /vagrant/catalog and installing
echo and activating the Python 3.7.1 environment
echo --------------------
cd /vagrant/catalog

virtualenv venv --python=python3.7
source /vagrant/catalog/venv/bin/activate

echo --------------------
echo Installing neccassary Python libraries for this applicaton
echo --------------------
sudo pip install -r requirements.txt

echo Python version:
python --version
echo Installed libraries:
pip freeze

echo --------------------
echo Create database and populate it with starter data
echo --------------------
python database_setup.py
python starter_data.py

echo --------------------
echo Launch Flask application on port 5000
echo --------------------
python project.py
