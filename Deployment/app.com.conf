<VirtualHost *:80>
         WSGIDaemonProcess app
     WSGIScriptAlias / /usr/local/app/Diablo3_project/Deployment/app.wsgi

     <Directory /usr/local/app/Diablo3_project/Interface>
            WSGIProcessGroup app
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
     </Directory>
</VirtualHost>