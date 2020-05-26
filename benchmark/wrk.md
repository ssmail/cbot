
### backend api benchmark test method and result

using `wrk` benchmark test tool, test command:
> wrk -t12 -c400 -d30s --latency http://localhost:5000/test_mem_cache

> -t thread number

> -c connection number

> -d duration time

> --latency print latency info after benchmark test

### test result:

cache read
- rt
- tps


db write
 
- rt
- tps


db read

- rt
-tps



