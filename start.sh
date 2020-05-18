pkill gunicron

git checkout .
git pull

nohup gunicorn wsgi:app -b :8000 -w 1 &

tail -f info.log
