# Diablo3_project
Retrieve Diablo 3 Leader Board Data. Analysis, Index and Visualize

Initialize an EC2 server and connect to it:

1. Go to EC2 Dashboard, select a region on the right top and launch a new Instance
2. Choose AMI, Instance Type; for configuration, may allow "Auto-assign Public IP" and when shut-down, stop the machine
3. For Security Group, can give new rule of "HTTP" as it is going to be a web server
4. Review everything, give a name to your pem key, store it in your local drive(keep safe) and launch the instance
5. If you are using Windows, download putty and puttygen online. In puttygen, load your pem key and save the private key(a ppk file) to your local drive
6. Open putty, for Host Name(or IP), right click your EC2 instance in EC2 dashboard, click connect. You will see an example that includes your server name and IP.(Mine is ubuntu@52.1.247.243)
7. Use default SSH connection, enter a name and save your configuration information. Under Data on the left bar, enter "root" as auto-login username; under SSH->Auth, browse your private key generated in step 5. Make sure you've saved all the information before open the connection
8. In ubuntu, the default username is "ubuntu"; for Free Tier info, check: https://aws.amazon.com/free/


Deploy Flask Application on EC2 ubuntu:

1. Install MongoDB:
sudo apt-get install mongodb
mongo -version

2. Python environment: 
http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-common-steps.html
(Note for ubuntu 14.04, python3.x is already installed, try "python3 -V" to check the version)

3. Install pip:
sudo apt-get update
sudo apt-get install python3-pip
pip3 -V

4. Install python modules:
sudo pip3 install requests 
sudo pip3 install beautifulsoup4
sudo pip3 install pymongo
sudo pip3 install diablo3api
sudo pip3 install Flask

5. Download source code on github:
sudo apt-get install git
cd /var/www
sudo git clone https://github.com/mochiliu3000/Diablo3_project


6. Run web crawler(use python3)
python3 D3CrawlerDemo.py
(This will automaticly create a new database in Mongodb called D3 and import top 100 leader board data from: http://us.battle.net/d3/en/rankings/era/2/rift-wd)

7. Deploy Flask website on Apache2 server: follow https://github.com/yolesaber/micromtn/blob/master/articles/HostingWithApache.md
sudo apt-get install apache2 libapache2-mod-wsgi
cd //var/www/Diablo3_project/Deployment

sudo nano app.wsgi
(Double check the path and name)
sudo nano app.com.conf
(Double check the path and name)
sudo mv app.com.conf /etc/apache2/sites-available/
(Move the app.com.conf to apache2 available site folder)

#from werkzeug.debug import DebuggedApplication
#app.debug = True
#app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
(In app.py, comment out these 3 lines to open the debug mode for wsgi module)

sudo a2dissite default
sudo a2ensite app.com
sudo /etc/init.d/apache2 restart
(Detach the default page and attach app.com; restart the server)

8. In web brower, enter Public DNS of the instance(Mine is "http://ec2-54-173-103-163.compute-1.amazonaws.com/") and test the website. If there are any server errors, can further check "error.log" under /var/log/apache2/
