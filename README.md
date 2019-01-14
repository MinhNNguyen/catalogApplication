## Movie Catalog Application

### Project Description
The base movie catalog application was first implemented in Vagrant virtual machine using Python Flask framework, SQLAlchemy, Bootstrap, and SQLite database. <br />
Later, the web application is updated to be hosted on Linux distribution virtual machine. This includes installing updates, configuring web and Postgresql database server, and implmenting securities against certain attack risks. <br />

IP Address: 54.184.72.93 <br />
SSH Port: 2200 <br />
EC2 URL is: http://ec2-54-184-72-93.us-west-2.compute.amazonaws.com/

### Configuration Step

1. Start an Ubuntu Linux server instance on Amazon Lightsail <br />
Choose Linux/Unix platform, Ubuntu 16.04 option <br />

2. Logging in as root and create a new user using sudo adduser grader with password. <br />
Then give grader user sudo permisson by typing visudo and set it up like this: <br />
root    ALL=(ALL:ALL) ALL <br />
grader ALL=(ALL:ALL) ALL <br />

3. Open SSHD config file by running sudo nano /etc/ssh/sshd_config and change SSH port from 22 to 2200. <br />
Configure the uncomplicated firewall by running these commands: <br />
sudo ufw default deny incoming <br />
sudo ufw default deny outgoing <br />
sudo ufw allow 2200/tcp <br />
sudo ufw allow 80/tcp <br />
sudo ufw allow 123/udp <br />
sudo ufw deny 22 <br />
sudo ufw enable <br />
Then you can check the status of the ufw by running sudo ufw status <br /> 

4. Generating key pair on local machine using applicaton ssh-keygen. Logging into your remote server, create .ssh folder and .ssh/authorized_keys in your home directory. Then copy content from .pub file generated from ssh-keygen into authorized_keys file that just being created. Set permission 700 to .ssh and 644 to authorized_keys file. <br />
Logging in to server using ssh -p 2200 -i ~./ssh/your_key_file. Set PasswordAuthentication to no and PermitRootLogin to no when opening sudo nano /etc/ssh/sshd_config file. Then run sudo service ssh restart to restart the service and force users to login using the key. <br />

5. Update all current installed packages by running apt-get update and apt-get upgrade. It is important to keep all the packages up to date since it is important for performance and security. <br />
If the system kept telling you that there are several packages and updates available. Run this command sudo apt-get update && sudo apt-get dist-upgrade. <br />

6. Configure the local timezone to UTC by running sudo dpkg-reconfigure tzdata and choose UTC <br />

7. Install and configure Apache2 and mod_wsgi application by running these commands: <br />
sudo apt-get install apache2 <br />
sudo apt-get install python-setuptools libapache2-mod-wsgi <br />
Later when running your applicaton, you might have trouble with version of mod wsgi. If that is the case, uninstall the wsgi mod compatible with other version of python if not using it. <br />

8. Install and configure databases for the application using PostgreSQL. Running these command below: <br />
sudo apt-get install postgresql postgresql-contrib
Login as postgres user using sudo su - postgres <br />
Starting PostgreSQL using psql <br />
Run CREATE USER catalog WITH PASSWORD 'password'; <br />
Give catalog user CREATEDB role ALTER USER catalog CREATEDB; <br />
Create catalog database using CREATE DATABASE catalog WITH OWNER catalog; <br />
Connect to catalog databse using \c catalog <br />
Revoke permission from public using REVOKE ALL ON SCHEMA public FROM public; <br />
Grant all permission to catalog user using GRANT ALL ON SCHEMA public TO catalog; <br />
Change the engine inside application to engine = create_engine('postgresql://catalog:password@localhost/catalog') <br />

9. Install git, clone, and make changes to the project to be able to use PostgreSQL <br />
Install git using sudo apt-get install git
Creating a new folder catalog and change the owner of the folder to grader using sudo chown -R grader:grader catalog <br />
Change directory to inside the folder and clone the project by using git clone https://github.com/MinhNNguyen/catalogApplication <br />
Add catalog.wsgi file with the following content <br/>
import sys <br/>
import logging <br/>
logging.basicConfig(stream=sys.stderr) <br/>
sys.path.insert(0, "/var/www/catalog/") <br/>

from catalogApplication import app as application <br/>

10. Create and configure Virtual Host <br />
Run sudo apt-get install python-virtualenv to install virtual environment <br />
Create new virtual environment using sudo virtualenv venv <br />
Activate using source venv/bin/activate and deactivate it using  deactivate <br />

11. Create and configure apache conf file <br />
Create a new config file for catalog web application using sudo nano /etc/apache2/sites-available/catalog.conf <br />
Adding the content below into the new config file <br />

<VirtualHost *:80>
    ServerName Public-IP-Address
    ServerAlias ec2-54-184-72-93.us-west-2.compute.amazonaws.com
    ServerAdmin admin-email
    WSGIDaemonProcess catalog python-path=/var/www/catalog:/var/www/catalog/venv/lib/python2.7/site-packages
    WSGIProcessGroup catalog
    WSGIScriptAlias / /var/www/catalog/catalog.wsgi
    <Directory /var/www/catalog/catalogApplication/>
        Order allow,deny
        Allow from all
    </Directory>
    Alias /static /var/www/catalog/catalogApplication/static
    <Directory /var/www/catalog/catalogApplication/static/>
        Order allow,deny
        Allow from all
    </Directory>
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

Enable the new virtual host using sudo a2ensite catalog <br />
Then start the apache2 server using sudo service apache2 start <br />

12. Accessing the server using: http://ec2-54-184-72-93.us-west-2.compute.amazonaws.com/ <br/>

### Built With

Python==2.7.12 <br />
apache2==2.4.18 <br />
Flask==1.0.2 <br />
Flask-SQLAlchemy==2.3.2 <br />
httplib2==0.12.0 <br />
itsdangerous==1.1.0 <br />
Jinja2==2.10 <br />
oauth2==1.9.0.post1 <br />
oauth2client==4.1.3 <br />
passlib==1.7.1 <br />
psycopg2==2.7.6.1 <br />
requests==2.9.1 <br />
SQLAlchemy==1.2.15 <br />
virtualenv==15.0.1 <br />

### Third Party Resources

URL: https://www.digitalocean.com/community/tutorials/how-to-set-up-apache-virtual-hosts-on-ubuntu-14-04-lts <br />
URL: https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps <br />
URL: https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps <br />
URL: https://www.digitalocean.com/community/tutorials/how-to-add-and-delete-users-on-an-ubuntu-14-04-vps <br />
URL: https://www.digitalocean.com/community/tutorials/how-to-tune-your-ssh-daemon-configuration-on-a-linux-vps <br />
URL: https://serverfault.com/questions/265410/ubuntu-server-message-says-packages-can-be-updated-but-apt-get-does-not-update <br />
URL: https://httpd.apache.org/docs/2.4/vhosts/name-based.html <br />
URL: http://manpages.ubuntu.com/manpages/xenial/en/man5/sshd_config.5.html <br />

### Useful commandline commands
If you want to debug server error: sudo tail -50 /var/log/apache2/error.log <br />
If you want to debug virtual host configuration: apachectl -S <br />


### Authors

Robert Nguyen