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

3. Set SSH login using key <br />

4. Update all current installed packages <br />

5. Change the SSH port from 22 to 2200 and configure the uncomplicated firewall <br />

6. Configure the local timezone to UTC <br />

7. Install and configure Apache2 and mod_wsgi application <br />

8. Install and configure databases for the application using PostgreSQL <br />

9. Install git, clone, and make changes to the project to be able to use PostgreSQL <br />

10. Create and configure Virtual Host <br />

11. Create and configure the catalog.wsgi file to <br />

12. Restart the apache2 server <br />


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

### Useful commandline commands
sudo tail -50 /var/log/apache2/error.log <br />
sudo tail -50 /var/log/apache2/access.log <br />

### Authors

Robert Nguyen