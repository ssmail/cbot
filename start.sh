git checkout .
git pull
pkill gunicorn

nohup gunicorn mantis_server:mantis_server -b :8000 -w 1 &