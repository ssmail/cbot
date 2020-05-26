Flask as a backend service

basic infra service such as:

* mq
* celery ansync task
* benchmark test


1、 Start redis

```redis-server```

2、 Start Redis admin

```redis-commander```

3 Start celery worker

```celery -A mantis worker -l info```

4 Start celery worker monitor

```flower -A mantis```


5 download & install kafka from github

``` wget https://codeload.github.com/dpkp/kafka-python/zip/master```

``` pip3 install kafka.zip```