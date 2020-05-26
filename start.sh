git checkout .
git pull
pkill gunicorn

gunicorn server:app -b :8000 -w 1

#nohup gunicorn -c config.py server:app &