# Diablo3_project


### Initialize an EC2 server and connect to it:

1. Go to EC2 Dashboard, select a region on the right top and launch a new Instance<br>
2. Choose AMI, Instance Type; for configuration, may allow "Auto-assign Public IP" and when shut-down, stop the machine<br>
3. For Security Group, can give new rule of "HTTP" as it is going to be a web server<br>
4. Review everything, give a name to your pem key, store it in your local drive(keep safe) and launch the instance<br>
5. If you are using Windows, download putty and puttygen online. In puttygen, load your pem key and save the private key(a ppk file) to your local drive<br>
6. Open putty, for Host Name(or IP), right click your EC2 instance in EC2 dashboard, click connect. You will see an example that includes your server name and IP.(Mine is ubuntu@52.1.247.243)<br>
7. Use default SSH connection, enter a name and save your configuration information. Under Data on the left bar, enter "root" as auto-login username; under SSH->Auth, browse your private key generated in step 5. Make sure you've saved all the information before open the connection<br>
8. In ubuntu, the default username is "ubuntu"; for Free Tier info, check: https://aws.amazon.com/free/

----

### Deploy Flask Application on EC2 ubuntu:
1. Install MongoDB:<br>
sudo apt-get install mongodb<br>
mongo -version<br>
2. Python environment: <br>
http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-common-steps.html<br>
(Note for ubuntu 14.04, python3.x is already installed, try "python3 -V" to check the version)<br>
3. Install pip:<br>
sudo apt-get update<br>
sudo apt-get install python3-pip<br>
pip3 -V<br>
4. Install python modules:<br>
sudo pip3 install requests <br>
sudo pip3 install beautifulsoup4<br>
sudo pip3 install pymongo<br>
sudo pip3 install diablo3api<br>
sudo pip3 install Flask<br>
5. Download source code on github:<br>
sudo apt-get install git<br>
cd /var/www<br>
sudo git clone https://github.com/mochiliu3000/Diablo3_project<br>
6. Run web crawler(use python3)<br>
python3 D3CrawlerDemo.py<br>
(This will automaticly create a new database in Mongodb called D3 and import top 100 leader board data from:<br> http://us.battle.net/d3/en/rankings/era/2/rift-wd)<br>
7. Deploy Flask website on Apache2 server: follow https://github.com/yolesaber/micromtn/blob/master/articles/HostingWithApache.md<br>
sudo apt-get install apache2 libapache2-mod-wsgi<br>
cd /var/www/Diablo3_project/Deployment<br>
sudo nano app.wsgi<br>
(Double check the path and name)<br>
sudo nano app.com.conf<br>
(Double check the path and name)<br>
sudo mv app.com.conf /etc/apache2/sites-available/<br>
(Move the app.com.conf to apache2 available site folder)<br>
 #from werkzeug.debug import DebuggedApplication<br>
 #app.debug = True<br>
 #app.wsgi_app = DebuggedApplication(app.wsgi_app, True)<br>
(In app.py, comment out these 3 lines to open the debug mode for wsgi module)<br>
sudo a2dissite default<br>
sudo a2ensite app.com<br>
sudo /etc/init.d/apache2 restart<br>
(Detach the default page and attach app.com; restart the server)<br>
8. In web brower, enter Public DNS of the instance(Mine is "http://ec2-54-173-103-163.compute-1.amazonaws.com/") and test the website. If there are any server errors, can further check "error.log" under /var/log/apache2/
