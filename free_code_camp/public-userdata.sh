#!/usr/bin/env bash
su ec2-user
sudo yum install httpd -y
sudo service httpd start
sudo su "cat > /var/www/html/index.html <<EOL
<html>
    <head>
    <title>Call to arms</title>
    <style>
        html, body {background: #000; padding: 0; margin: 0; }
        img { display: block; margin: 0px auto; }
    </style>
    </head>
    <body>
        <img src='https://giphy.com/gifs/nfl-sports-football-sport-l6BIKJMz60Sz2Ai4U1' height='100%'/>
    </body>
</html>
EOL"
