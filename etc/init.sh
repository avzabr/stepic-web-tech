#!/usr/bin/env bash
sudo cp -r /home/box/stepic-web-tech/ /home/box/web/
sudo ln -sf /home/box/web/etc/hello.py /etc/gunicorn.d/hello.py
sudo ln -sf /home/box/web/etc/hello.py /home/box/web/hello.py
gunicorn -b 0.0.0.0:8080 hello:hello &
sudo ln -sf /home/box/web/etc/nginx.conf  /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart