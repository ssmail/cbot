git checkout .
git pull
pkill gunicorn

gunicorn mantis_server:mantis_server -b :8000 -w 1
