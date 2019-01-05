# Udacity_FSND_Project_Four: Linux Server Configuration

### This is project number four from the Udacity Full Stack Web Developer Nanodegree Program
## Project overview:
* Take a baseline installation of a Linux server and prepare it to host your web applications. You will secure your server from a number of attack vectors, install and configure a database server, and deploy one of your existing web applications onto it.

## Purpose of this project:
* To obtain a deep understanding of exactly what your web applications are doing, how they are hosted, and the interactions between multiple systems are what define you as a Full Stack Web Developer. In this project, you’ll be responsible for turning a brand-new, bare bones, Linux server into the secure and efficient web application host your applications need.

## Aside:
***This was a very challenging and frustrating experience completing this project and as such I wanted this README to act
as sort of a guide for anyone that may come across it. I have been successfully building and deploying LAMP 
and LEMP servers (not with Flask) for a few years now and have not faced the same amount of challenges and failures 
since building my first public facing web server. That being said, upon successfully working through all of these 
challenges and finally launching the Project 3 Flask Catalog app successfully, I was very proud of my success and 
learned a TON along the way. So if anyone is viewing this project on GitHub and is at their wits end...please don't 
give up! Specifically, the OAuth portion of the Flask app caused significant headaches (due mostly to my lack of 
understanding of the intricacies of the software) and the uWSGI portion of serving my Flask app (this led to hours 
and hours of Google research). However, all of the time I spent troubleshooting issues led to a much greater 
understanding of the Flask architecture and all of the moving parts that allow the Flask application to be served on 
a public IP.*** 

## VPS Server Details and Software:
* This web server was built using a Digital Ocean 1GB Droplet: [Digital Ocean Plans](https://www.digitalocean.com/pricing/)
* IP Address: 206.189.228.165
* Flask App URL: http://wickkwired.com
* Operating System: Ubuntu 18.04LTS x64
* Nginx Version: nginx/1.14.0 (Ubuntu)
* PostgreSQL 10.6 (Ubuntu 10.6-0ubuntu0.18.04.1)
* Python 3.6.7 (installed by default on the Digital Ocean Ubuntu 18.04 Droplet)
* I have used the domain name (wickkwired.com) that I have owned for years and was not being utilized
* As I have used [Linode](https://www.linode.com/) ***(I love Linode, but I really relied heavily on Digital Ocean's Flask 
guide for this project so I thought it only fair to give them the business this time 'round)*** as my primary VPS and 
DNS service for years, I utilized their Name Servers to point my domain name to the newly created Droplet....yikes (sorry guys!)

## Helpful guides and resources utilized for this project:
* [Digital Ocean: Ubuntu 18.04 Initial Server Setup Guide](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04)
* [Digital Ocean: How To Install Nginx on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04)
* [Digital Ocean: How To Serve Flask Applications with uWSGI and Nginx on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04)
* [stackoverflow: secret key not set in flask session, using the Flask-Session extension](https://stackoverflow.com/questions/26080872/secret-key-not-set-in-flask-session-using-the-flask-session-extension)

## Python Software Requirements 
* certifi==2018.11.29
* chardet==3.0.4
* Click==7.0
* dominate==2.3.5
* Flask==1.0.2
* Flask-Bootstrap==3.3.7.1
* httplib2==0.12.0
* idna==2.8
* itsdangerous==1.1.0
* Jinja2==2.10
* MarkupSafe==1.1.0
* oauth2client==4.1.3
* pkg-resources==0.0.0
* psycopg2==2.7.6.1
* psycopg2-binary==2.7.6.1
* pyasn1==0.4.4
* pyasn1-modules==0.2.2
* requests==2.21.0
* rsa==4.0
* six==1.12.0
* SQLAlchemy==1.2.15
* urllib3==1.24.1
* uWSGI==2.0.17.1
* visitor==0.1.3
* Werkzeug==0.14.1

## Steps to satisfying the project rubric:
### Step 1: Update all currently installed packages:
```bash
# Logged in as root:
apt update && apt upgrade
```
### Step 2: Create new limited user account named 'grader':
```bash
adduser grader
...
usermod -aG sudo grader
```
***Please note, out of habit and a security best practice I like to adhere to, I did not allow the new user to run 
sudo commands without a password ("think twice, sudo once"). To do so I could have made and added the following entry 
/etc/sudoers.d/grader :***
```bash
touch /etc/sudoers.d/grader && echo "grader ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/grader
```
### Step 3: Modify server hostname and /etc/hosts file to utilize DNS (I am only using IPv4 on this server):
```bash
hostnamectl set-hostname wickkwired.com
vim /etc/hosts
# add the following:
127.0.1.1 wickkwired.com wickkwired
127.0.0.1 localhost
206.189.228.165 wickkwired.com wickkwired
```
***UTC time is enabled by default, as per the project requirements this was left as is but could be configured using 
the following command***
```bash
dpkg-reconfigure tzdata
```

### Step 4: Log out root user and log back in with grader account, set up SSH Keys:
```bash
ssh grader@wickkwired.com
```
**OR**
```bash
ssh grader@206.189.228.165
```
* Create .ssh directory and modify permissions:
```bash
mkdir -p ~/.ssh && sudo chmod -R 700 ~/.ssh/
```

* Creating SSH Key pair locally on personal MacBook Pro and secure copying Public key to Droplet:
```bash
ssh-keygen -b 4096
scp ~/.ssh/id_rsa.pub grader@wickkwired.com:~/.ssh/authorized_keys
```
* Back on Droplet, modify .ssh/ and .ssh/authorized_keys permissions:
```bash
sudo chmod -R 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys
```

### Step 5: Change SSH port to 2200 disable root login and allow SSH key-pair access only:
```bash
sudo vim /etc/ssh/sshd_config
```
* Change the following:
```bash
#Port 22
#AddressFamily any
#ListenAddress 0.0.0.0
#ListenAddress ::
...
#LoginGraceTime 2m
PermitRootLogin yes
#StrictModes yes
#MaxAuthTries 6
#MaxSessions 10
...
# To disable tunneled clear text passwords, change to no here!
PasswordAuthentication yes
#PermitEmptyPasswords no

```
* To:
```bash
Port 2200
#AddressFamily any
#ListenAddress 0.0.0.0
#ListenAddress ::
...
#LoginGraceTime 2m
PermitRootLogin no
#StrictModes yes
#MaxAuthTries 6
#MaxSessions 10
...
# To disable tunneled clear text passwords, change to no here!
PasswordAuthentication no
#PermitEmptyPasswords no
```
* Restart the sshd service to put rules into effect:
```bash
sudo systemctl restart sshd
```
* Log out of the server and log back in using ssh keys on port 2200
```bash
ssh grader@wickkwired.com -p 2200
```

### Step 6: Configure UFW Firewall as per rubric:
***Note - custom firewall configurations were made for Nginx to work properly later on***
```bash
sudo ufw status
Status: inactive

sudo ufw default deny incoming
Default incoming policy changed to 'deny'
(be sure to update your rules accordingly)

sudo ufw default allow outgoing
Default outgoing policy changed to 'allow'

sudo ufw allow 2200/tcp
Rules updated
Rules updated (v6)

sudo ufw allow www
Rules updated
Rules updated (v6)

sudo ufw allow ntp
Rule added
Rule added (v6)

sudo ufw enable
Command may disrupt existing ssh connections. Proceed with operation (y|n)? y
Firewall is active and enabled on system startup

sudo ufw status
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     DENY        Anywhere
2200/tcp                   ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
Nginx HTTP                 ALLOW       Anywhere
Nginx Full                 ALLOW       Anywhere
123                        ALLOW       Anywhere
22                         DENY        Anywhere
22/tcp (v6)                DENY        Anywhere (v6)
2200/tcp (v6)              ALLOW       Anywhere (v6)
80/tcp (v6)                ALLOW       Anywhere (v6)
Nginx HTTP (v6)            ALLOW       Anywhere (v6)
Nginx Full (v6)            ALLOW       Anywhere (v6)
123 (v6)                   ALLOW       Anywhere (v6)
22 (v6)                    DENY        Anywhere (v6)
```

## Step 7: Install and Configure PostgreSQL:
```bash
sudo apt install libpq5 postgresql
sudo -i -u postgres
postgres@wickkwired:~$ psql
psql (10.6 (Ubuntu 10.6-0ubuntu0.18.04.1))
Type "help" for help.

postgres=CREATE USER catalog WITH PASSWORD 'grader';
CREATE ROLE
postgres=ALTER USER catalog CREATEDB;
ALTER ROLE
postgres=CREATE DATABASE catalog WITH OWNER catalog;
CREATE DATABASE
postgres=\c catalog
You are now connected to database "catalog" as user "postgres".
catalog=REVOKE ALL ON SCHEMA public FROM public;
REVOKE
catalog=GRANT ALL ON SCHEMA public TO catalog;
GRANT
catalog=\q
postgres@wickkwired:~$ exit
```
# Note: These next steps utilize the following Digital Ocean guides pretty much to a "T":
* [Digital Ocean: How To Install Nginx on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04)
* [Digital Ocean: How To Serve Flask Applications with uWSGI and Nginx on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04)

## Step 8: Install Nginx:
```bash
sudo apt install nginx
sudo ufw allow 'Nginx HTTP'
```

## Step 9: Install Flask, uWSGI, and additional project dependancies. Clone Catalog project, make configuration changes and launch Flask Application
```bash
cd
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
sudo apt install python3-venv
git clone https://github.com/thewickk/Udacity_FSND_Project_Two.git fsndproject
cd fsndproject/
python3.6 -m venv fsndenv
source fsndenv/bin/activate
pip install wheel
pip install -r requirements.txt

```
* Modify project.py, database_setup.py, and starter_data.py to user PostgreSQL instead of Sqlite3:

<u>Change:</u>
```bash
engine = create_engine('sqlite:///database.db')
```
<u>To:</u>
```bash
engine = create_engine('postgresql://catalog:grader@localhost/catalog')
```
* Populate PostgreSQL database with app data:
```bash
python database_setup.py
python starter_data.py
```
* Create WSGI Entry Point
```bash
nano wsgi.py
# Add these contents:
from project import app

if __name__ == "__main__":
    app.run()
```
* Create a uWSGI Cofiguration File:
```bash
nano fsndproject.ini
# Add these contents:
[uwsgi]
module = wsgi:app

master = true
processes = 5

socket = fsndproject.sock
chmod-socket = 660
vacuum = true

die-on-term = true
```
* Create systemd Unit File for automatic uWSGI startup to serve Flask app:
```bash
nano /etc/systemd/system/fsndproject.service
# Add these contents:
[Unit]
Description=uWSGI instance to serve Udacity FSND Project 4
After=network.target

[Service]
User=grader
Group=www-data
WorkingDirectory=/home/grader/fsndproject
Environment="PATH=/home/grader/fsndproject/fsndenv/bin"
ExecStart=/home/grader/fsndproject/fsndenv/bin/uwsgi --ini fsndproject.ini

[Install]
WantedBy=multi-user.target
```
* Start the newly created systemd service and make it persistent:
```bash
sudo systemctl start fsndproject
sudo systemctl enable fsndproject
```
* Create an Nginx server block to server our application on port 80 using the DNS entry ***wickkwired.com***
```bash
sudo nano /etc/nginx/sites-available/wickkwired.com
# Add these contents:
server {
    listen 80;
    server_name wickkwired.com www.wickkwired.com;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/grader/fsndproject/fsndproject.sock;
    }
}
```
* Restart nginx and open up the UFW firewall for Nginx:
```bash
sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'
```

* Website is accessible at the following URLs:
http://www.wickkwired.com
http://wickkwired.com

## Notes, Troubleshooting, and Errors:
### The following error plagued me for days...
```bash
RuntimeError: The session is unavailable because no secret key was set. Set the secret_key on the application to 
something unique and secret.
```
* After days of trying to understand this error and where to put my secret_key I finally found the solution by adding 
the following to the main Flask app file: project.py - 
```python
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super_secret_key'
```
***This is the stackoverflow entry that solved my issue:***

[stackoverflow: secret key not set in flask session, using the Flask-Session extension](https://stackoverflow.com/questions/26080872/secret-key-not-set-in-flask-session-using-the-flask-session-extension)

### The other big trouble spot for me was getting Google OAuth 2.0 to work...
***I never did figure out how to get OAuth 2.0 to work without having a valid DNS entry. After hours of changing 
Authorized JavaScript origins and Authorized redirect URIs and re-inserting updated client_secrets.json into my project
to no avail, I opted to use a valid domain name that I already own. After adding the following to my Google OAuth 2.0
project client ID and downloading the newly created JSON file I finally was able to get OAuth to work:***

### <u>Authorized JavaScript origins</u> 
***Please note that for these entries that www. was left out. I encountered countless 400 errors due to the fact that 
I was using http://www.wickkwired.com***
```bash
# For dev testing:
http://wickkwired.com:5000  
# For production:
http://wickkwired.com
```
### <u>Authorized redirect URIs</u>
```bash
# For dev testing:
http://wickkwired.com:5000/login
http://wickkwired.com:5000/gconnect
# For production:
http://wickkwired.com/login
http://wickkwired.com/gconnect
```
