git checkout .
git pull
pkill gunicorn

python3.7 server.py

# nohup gunicorn -c config.py server:app &

