#!/usr/bin/env bash
sudo cp -r /home/box/stepic-web-tech/ /home/box/web/

#gunicorn hello wsgi
sudo ln -sf /home/box/web/etc/hello.py /home/box/web/hello.py
sudo ln -sf /home/box/web/etc/gunicorn.hello.conf /etc/gunicorn.d/hello

#gunicorn django
sudo ln -sf /home/box/web/etc/gunicorn.ask.conf /etc/gunicorn.d/ask

sudo /etc/init.d/gunicorn restart

#nginx
sudo ln -sf /home/box/web/etc/nginx.conf  /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart