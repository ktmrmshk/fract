<!-- 
__CMD__
__NAME__
__CONTAINER__

$ cat README_SRC.md | sed -e 's/__CMD__/sprett/g' | sed -e 's/__NAME__/sprett/g' | sed -e 's/__CONTAINER__/sprett/g' > README.md
-->

__NAME__
=============

A web tool for CDN regression test


Overview
-------------

A web tool for CDN regression test


Installation
------------

### Docker Image

Faster and handy way to quickly start.

```
$ docker pull ktmrmshk/__CONTAINER__

$ docker run -it ktmrmshk/__CONTAINER__ /bin/bash

root@3f10471d9422:/# __CMD__ -h
usage: __CMD__ [-h] [-v] [--version]
             {geturlc,geturlakm,testgen,run,tmerge,rmerge,j2y,y2j,redirsum,ercost,testredirectloop,worker,testgen_pls,run_pls,wait_mq_ready}
             ...

positional arguments:
  {geturlc,geturlakm,testgen,run,tmerge,rmerge,j2y,y2j,redirsum,ercost,testredirectloop,worker,testgen_pls,run_pls,wait_mq_ready}
                        sub-command help
    geturlc             Get URL list using built-in crawler
    geturlakm           Get URL list using Akamai Top Url List CSV files
    testgen             Testcase generator based on current server's behaviors
    run                 Run testcases
    tmerge              Merge multiple testcases into signle file
    rmerge              Merge multiple results into signle form
    j2y                 Json to yaml converter
    y2j                 Yaml to json converter
    redirsum            Export redirect request/response summary in JSON form
    ercost              Export Eege-Redirector-Cost summary in JSON form
    testredirectloop    Test if redirect happend more than special value
    worker              spawn a worker and subscribe task queue
    testgen_pls         execute 'testgen' command in parallel using __CMD__
                        workers
    run_pls             execute 'run' command in parallel using __CMD__ workers
    wait_mq_ready       Check if mq server is ready

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbosity       verbos display
  --version             verion info
```

Changelog
------------

* 2018/07/31 - custom request header support
* 2018/08/15 - redirect summary, Edge-Redirector-Cost check	
* 2018/08/22 - Ignore-case option support
* 2018/12/04 - changed request generating testcase to avoid Rum-on/off mismatches test failuer
* 2019/03/29 - v0.7 Ignore x-check-cacheable value when 30x redirect response, version info support
* 2019/04/15 - v0.8 Redirect Loop Detection - testredirectloop option
* 2019/06/17 - v1.0 parallelization by __CMD__ worker
  - Fract worker `__CMD__ woker`, `__CMD__ testgen_pls` and `__CMD__ run_pls` command are introduced to run process in parallel. 
  - No check on `X-Check-Cacheable` header by default as it's not reliable checkpoint. Use `__CMD__ testgen --strict-check-cacheability` if you need to check `X-Check-Cacheable`.
  - Testcase and result (JSON format) changed to have new field `LoadTime` and `Comment`, which contains actual laoding time at request and generator's info respectively.
  
  

Workflow Example 1 - Basic usage with single prcess
------------

### 1. Collect URL list

#### A. Using crawler

Testcase is generated based on specific URL, so that you need to collect URLs and put it together single text file.
Fract helps collect URLs using built-in crawler.

```
$ __CMD__ geturlc -e https://www.abc123.com/ -d 1 -o urllist.txt -D www.abc123.com
```

Show help to get more details:

```
$ __CMD__ geturlc -h

usage: __CMD__ geturlc [-h] -e ENTRYPOINT [-d DEPTH] -o OUTPUT -D DOMAIN
                     [DOMAIN ...]

optional arguments:
  -h, --help            show this help message and exit
  -e ENTRYPOINT, --entrypoint ENTRYPOINT
                        entry point url e.g. https://www.akamai.com/
  -d DEPTH, --depth DEPTH
                        depth of crawling. default=1
  -o OUTPUT, --output OUTPUT
                        output filename
  -D DOMAIN [DOMAIN ...], --domain DOMAIN [DOMAIN ...]
                        domain/FQDN to collect. e.g. www.akamai.com
                        www2.akamai.com ...
```



This command generates URL list file with name you specified in command line.

```
$ ls
urllist.txt

$ less urllist.txt
https://www.abc123.com/
http://www.abc123.com/jp/
http://www.abc123.com/jp/sp/
http://www.abc123.com/jp/css/abc123.css
http://www.abc123.com/jp/css/20151215_normalize.css
http://www.abc123.com/jp/css/top-140509.css
...
...
```

#### B. Using Akamai top url csv files

If akamai top url csv files are available, testcase can be made from that.

```
$ __CMD__ geturlakm -i top_u_r_l_hits_1.csv top_u_r_l_hits_2.csv -D www.abc123.com -p https -o urllist.txt
```

Akamai's log doesn't contains protocol info and FQDN, so that you must specify these params.





### 2. Make testcases from URL list

Next step is making testcase from URL list. To this end, you need to know the hostname or IP address of both

* webserver/ghost that you refer as a original/base bahavior - refered as "source ghost"
* webseever/ghost that you try to test - refered as "destination/target ghost"

Usually, production server is used as source ghost and staging server is used as dest ghost.
At akamaized domain, these hostnames can be found using `dig` command.

```
$ dig www.abc123.com

;; ANSWER SECTION:
www.abc123.com.   15011 IN  CNAME www.abc123.com.edgekey.net.
www.abc123.com.edgekey.net. 7811 IN CNAME www.abc123.com.edgekey.net.globalredir.akadns.net.
www.abc123.com.edgekey.net.globalredir.akadns.net. 1376 IN CNAME e1234.b.akamaiedge.net.
e1234.b.akamaiedge.net. 17  IN  A 23.210.235.187
```

In this case, source server is `www.abc123.com.edgekey.net`, while dest server is `e1234.b.akamaiedge-staging.net`.
With that, testgeases can be generated as follows.

```
$ __CMD__ -v testgen -i urllist.txt -o testcase.json -s www.abc123.com.edgekey.net -d e1234.b.akamaiedge-staging.net
```


If you like to modify or append custom request header like User-Agent and Referer, use `-H` option with json-formatted custom headers and values.


```
$ __CMD__ -v testgen -H '{"User-Agent": "iPhone", "Referer": "http://www.abc.com/"}' -i urllist.txt -o testcase.json -s www.abc123.com.edgekey.net -d e1234.b.akamaiedge-staging.net 

$ ls
testcase.json urllist.txt

$ less testcase.json

[{"TestType": "hassert", "Request": {"Ghost": "e1234.b.akamaiedge-staging.net", "Method": "GET", "Url": "https://www.abc123.com/", " Headers": {"Pragma": "akamai-x-cache-on,akamai-x-cache-remote-on,akamai-x-
...
...
```


### 3. Run testcases

Run testcases, then you can get summary and full result data.

```
$ __CMD__ -v run -i testcase.json

Summary
=================

Tests not passed
----------------
### TestId: 7602767a85e909990f7c5154f4464c89dfe74ad34f8cfcc55f20efa3b1af9a36

Request:
  Ghost: e1234.b.akamaiedge-staging.net
  Headers:
    Pragma: akamai-x-cache-on,akamai-x-cache-remote-on,akamai-x-check-cacheable,akamai-x-get-cache-key,akamai-x-get-extracted-values,akamai-x-get-request-id,akamai-x-serial-no,
      akamai-x-get-true-cache-key
  Method: GET
  Url: https://www.abc123.com/

status_code:
- Passed: false
  Response: 302
  TestAssert: 'regex: "301"'



Total
----------------
ran 181 tests: 1 failed

=> Not Good
```

In this case, 181 tests ran, and one test failed.

Summary(frsummaryxxxx.txt), full result data(fretxxxxx.json) and testcases that failed at this run (frdiffxxxxx.yaml) are generated separately.

```
$ ls
frdiff20180523141553196655.yaml   <== failed testcases
frsummary20180523141553196655.txt  <== summary
fret20180523141553196655.json  <== full result data
urllist.txt
testcase.json
```



### 4. Change failed testcases 


The failed testcases file is yaml format so that you can read and edit handily. By checking the summary, edit and fix this failed testcases.

```
$ vim frdiff20180523141553196655.yaml

- Comment: This test was gened by FraseGen
  Request:
    Ghost: e1234.b.akamaiedge-staging.net
    Headers:
      Pragma: akamai-x-cache-on,akamai-x-cache-remote-on,akamai-x-check-cacheable,akamai-x-get-cache-key,akamai-x-get-extracted-values,akamai-x-get-request-id,akamai-x-serial-no,
        akamai-x-get-true-cache-key
    Method: GET
    Url: https://www.abc123.com/
  TestCase:
    Location:
    - query: http://www.abc123.com/jp/
      type: regex
    X-Cache-Key:
    - query: /27115/
      type: regex
    - query: /30d/
      type: regex
    X-Check-Cacheable:
    - query: 'NO'
      type: regex
    status_code:
    - query: '302'   <==== EDIT!!!! from 301 to 302 !
      type: regex
  TestId: 7602767a85e909990f7c5154f4464c89dfe74ad34f8cfcc55f20efa3b1af9a36
  TestType: hassert
```

### 5. Re-run failed test only

First, convert to json before retrying.

```
$ __CMD__ y2j frdiff20180523141553196655.yaml frdiff20180523141553196655.json
```

Then, it's time to re-run.

```
$ __CMD__ -v run -i frdiff20180523141553196655.json
Summary
=================

Tests not passed
----------------

Total
----------------
ran 1 tests: 0 failed

=> OK
```

New test summary and result files will be genearated.

```
$ ls
frdiff20180523141553196655.json
frdiff20180523141553196655.yaml
frdiff20180523142335107496.yaml <== Added !
fret20180523141553196655.json
fret20180523142335107496.json <== Added ! 
frsummary20180523141553196655.txt
frsummary20180523142335107496.txt <== Added !
testcase.json
urllist.txt
```


### 6. Merge results

After all testcases passed the test, merge and put all results together for a permanent record.

```
$ __CMD__ rmerge -t testcase.json frdiff*.json -r fret* -s final_summary.txt -o final_result.json

Summary
=================

Tests not passed
----------------

Total
----------------
ran 181 tests: 0 failed

=> OK


$ ls -l
final_result.json <== Added
final_summary.txt <== Added
frdiff20180523141553196655.json
frdiff20180523141553196655.yaml
frdiff20180523142335107496.yaml
fret20180523141553196655.json
fret20180523142335107496.json
frsummary20180523141553196655.txt
frsummary20180523142335107496.txt
testcase.json
urllist.txt
```



### 7. Merge testcases

Finally, merge testcases into signle file for next round.

```
$ __CMD__ tmerge -t testcase.json frdiff*.json -o final_testcase.json 

$ ls -l
final_result.json
final_summary.txt
final_testcase.json                 <== Added !
frdiff20180523141553196655.json
frdiff20180523141553196655.yaml
frdiff20180523142335107496.yaml
fret20180523141553196655.json
fret20180523142335107496.json
frsummary20180523141553196655.txt
frsummary20180523142335107496.txt
testcase.json
urllist.txt
```


### 8. Export redirect summary

Summary on redirect request/response can be parsed from test result.

```
$ __CMD__ redirsum -t final_testcase.json -r final_result.json -o redirect_summary.json

$ ls -l
final_result.json
final_summary.txt
final_testcase.json
frdiff20180523141553196655.json
frdiff20180523141553196655.yaml
frdiff20180523142335107496.yaml
fret20180523141553196655.json
fret20180523142335107496.json
frsummary20180523141553196655.txt
frsummary20180523142335107496.txt
redirect_summary.json                 <== Added !
testcase.json
urllist.txt

$ cat redirect_summary.json 
[
  {
    "Request": {
      "Url": "http://fract.akamaized.net/single-video.html",
      "Method": "GET",
      "Ghost": "fract.akamaized-staging.net",
      "Headers": {}
    },
    "TestPassed": true,
    "Response": {
      "status_code": 301,
      "Server": "AkamaiGHost",
      "Location": "https://fract.akamaized.net/single-video.html",
      "X-Akamai-Tapioca-Cost-ER": "10031926"
    },
    "TestId": "631799cd2875b35de51ac45d0a4c8627c06d16cbf1f511dcaadd725d9f0d182b"
  },
  {
    "Request": {
      "Url": "https://fract.akamaized.net/pm_redirect/abc123",
      "Method": "GET",
      "Ghost": "fract.akamaized-staging.net",
      "Headers": {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
      }
    },
    "TestPassed": true,
    "Response": {
      "status_code": 302,
      "Server": "AkamaiGHost",
...
...
``` 

### 9. Edge-Redirector-Cost check

Similarly, Edge-Redirector-Cost can be checked from test result. To list up requests of Edge-Redirector-Cost over 1000000, type as follows:

```
$ __CMD__ ercost -c 1000000 -t final_testcase.json -r final_result.json -o ercost_summary.json.test

$ ls -l 
final_result.json
final_summary.txt
final_testcase.json
frdiff20180523141553196655.json
frdiff20180523141553196655.yaml
frdiff20180523142335107496.yaml
fret20180523141553196655.json
fret20180523142335107496.json
frsummary20180523141553196655.txt
frsummary20180523142335107496.txt
redirect_summary.json
ercost_summary.json.test                 <== Added !
testcase.json
urllist.txt



$ cat ercost_summary.json.test
[
  {
    "Request": {
      "Url": "https://fract.akamaized.net/",
      "Method": "GET",
      "Ghost": "fract.akamaized-staging.net",
      "Headers": {}
    },
    "TestPassed": true,
    "Response": {
      "status_code": 200,
      "Server": "Apache",
      "Location": "",
      "X-Akamai-Tapioca-Cost-ER": "10041225"
    },
    "TestId": "5e01096573d3757e1a669e4cbf3207f7ebc1e11df3ebf0c0226429c35dbf4668"
  },
  {
    "Request": {
      "Url": "http://fract.akamaized.net/single-video.html",
      "Method": "GET",
      "Ghost": "fract.akamaized-staging.net",
      "Headers": {}
    },
    "TestPassed": true,
    "Response": {
      "status_code": 301,
      "Server": "AkamaiGHost",
      "Location": "https://fract.akamaized.net/single-video.html",
      "X-Akamai-Tapioca-Cost-ER": "10031926"
    },
    "TestId": "631799cd2875b35de51ac45d0a4c8627c06d16cbf1f511dcaadd725d9f0d182b"
  },
...
...

```


### 10. Next round

Go to #1, #2 or #3.




Redirect Loop Detection Example - Usage
------------

Use `__CMD__ testredirectloop` command to check if there's redirect loop in the url list.
`__CMD__ testredirectloop` has following options:

```
$ __CMD__ testredirectloop -h
usage: __CMD__ testredirectloop [-h] -i INPUT [-o OUTPUT] [-s SUMMARY]
                              [-d DSTGHOST] [-m MAXIMUM]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input filename containing url list
  -o OUTPUT, --output OUTPUT
                        filename for full result output
  -s SUMMARY, --summary SUMMARY
                        filename for summary output
  -d DSTGHOST, --dstghost DSTGHOST
                        dest ghost/webserver name. This is optional. If not
                        specified, it requests to web host based on URL in
                        inputfile.
  -m MAXIMUM, --maximum MAXIMUM
                        threshold to trace redirect chain. default=5
```

This `__CMD__ testredirectloop` detects redirect loop by chasing redirect recursively and if depth of redirect chase reaches some threshold, then takes it as *redirect loop*. Default threshold depth is `5`, which can be changed by `-m` option.

The input file, which is specified by `-i` option, is a text file in which URLs listed.

urllist.txt - example:
```
https://fract.akamaized.net/301/3/
https://fract.akamaized.net/307/6/
https://fract.akamaized.net/
```

To check redirect loop for this URL list `urllist.txt`, run the following command. Afterwards, you get the summary and detailed results as files.

```
$ __CMD__ testredirectloop -i urllist.txt 

Summary
=================
Condition
----------------
Maximum Value 5


Total
----------------
ran 3 tests: 2 redirect URLs , 1 failed

=> Not Good
https://fract.akamaized.net/307/6/
```

In this summary, this `__CMD__ testredirectloop` ran test on 3 URLs, detects 2 redirect URLs, and 1 redirect chain that exceeds threshold, which is default value `5` in this test.

The `__CMD__ testredirectloop` also export detailed results in files.

```
$ ls 
loopret20190415080457421844.json
loopsummary20190415080457421844.txt

$ cat loopret20190415080457421844.json
[
    {
        "Depth": 3,
        "TargetHost": "fract.akamaized.net",
        "Chain": [
            {
                "Location": "https://fract.akamaized.net/301/2/",
                "status_code": 301
            },
            {
                "Location": "https://fract.akamaized.net/301/1/",
                "status_code": 301
            },
            {
                "Location": "https://fract.akamaized.net/",
                "status_code": 301
            }
        ],
        "Threshold": 5,
        "ReachedThreshold": false,
        "URL": "https://fract.akamaized.net/301/3/"
    },
    {
        "Depth": 5,
        "TargetHost": "fract.akamaized.net",
        "Chain": [
            {
                "Location": "https://fract.akamaized.net/307/5/",
                "status_code": 307
            },
            {
                "Location": "https://fract.akamaized.net/307/4/",
                "status_code": 307
            },
            {
                "Location": "https://fract.akamaized.net/307/3/",
                "status_code": 307
            },
            {
                "Location": "https://fract.akamaized.net/307/2/",
                "status_code": 307
            },
            {
                "Location": "https://fract.akamaized.net/307/1/",
                "status_code": 307
            }
        ],
        "Threshold": 5,
        "ReachedThreshold": true,
        "URL": "https://fract.akamaized.net/307/6/"
    }
]
```

From this result, the URL `https://fract.akamaized.net/301/3/` has 3 redirect chains, while `https://fract.akamaized.net/301/6/` has more than 5 chains, which is chain threshold `fract testredirectloop` does.

To test on another webserver, e.g. Akamai staging edge server, specify the target webserver by `-d` option. For example, to test redirect loop on Akamai staging which hostname is `fract.akamaized-staging.net`, following command does that.

```
$ __CMD__ testredirectloop -i urllist.txt -d fract.akamaized-staging.net
```


Workflow Example 2 - Parallel execution by __NAME__ worker
------------

### Installation

In addition to docker execution enviromnent, 
[`docker-compose`](https://docs.docker.com/compose/) is requried to run in multi process fashion.
There's some ways to install docker-compose though, let's take `python pip` way here.
Visit the [Install Docker Compose](https://docs.docker.com/compose/install/) on alternative installation choice. 

```
$ python3 -m pip install docker-compose
```

### Workflow cycle

1. start __NAME__ workers up
2. run __NAME__ command (many times)
3. shutdown and cleanup __NAME__ worker

#### 1. start __NAME__ worker up

First, there's need to start __NAME__ workers up before executing __NAME__.

```
(from shell on your host machine)
### make working directory
$ mkdir test
$ cd test

### get docker-compose.yml
$ cp docker-compose/docker-compose.yml .
$ ls
docker-compose.yml  <=== downloaded!

### pull the docker container needed first
$ docker-compose pull

### finally, start up __NAME__ workers - 4 workers in this example
$ docker-compose up -d --scale worker=4

Creating test_rabbitmq_1 ... done
Creating test_mongodb_1  ... done
Creating test_fract_1    ... done
Creating test_worker_1   ... done
Creating test_worker_2   ... done
Creating test_worker_3   ... done
Creating test_worker_4   ... done
```

If you change the number of __NAME__ worker, which is equal to number of process in parallel execution, type same `docker-compose run` command at any time.

```
#### Change number of woker to 16
$ docker-compose up -d --scale worker=16
```


#### 2. run __CMD__ command (many times)

Then, run __NAME__ container and __CMD__ command in that container. Almost workflow is same as conventional fract execution, except for `testgen` and `run` commands. To execute `testgen` and `run` command in parallel, we use `testgen_pls` and `run_pls` command, which uses __NAME__ worker to run sub process like fetch HTTP request to web sever.

```
### start and enter __NAME__ container
$ docker-compose run __CMD__ /bin/bash

(entered container)
# __CMD__ -h

usage: __CMD__ [-h] [-v] [--version]
             {geturlc,geturlakm,testgen,run,tmerge,rmerge,j2y,y2j,redirsum,ercost,testredirectloop,worker,testgen_pls,run_pls,wait_mq_ready}
             ...

positional arguments:
  {geturlc,geturlakm,testgen,run,tmerge,rmerge,j2y,y2j,redirsum,ercost,testredirectloop,worker,testgen_pls,run_pls,wait_mq_ready}
                        sub-command help
    geturlc             Get URL list using built-in crawler
    geturlakm           Get URL list using Akamai Top Url List CSV files
    testgen             Testcase generator based on current server's behaviors
    run                 Run testcases
    tmerge              Merge multiple testcases into signle file
    rmerge              Merge multiple results into signle form
    j2y                 Json to yaml converter
    y2j                 Yaml to json converter
    redirsum            Export redirect request/response summary in JSON form
    ercost              Export Eege-Redirector-Cost summary in JSON form
    testredirectloop    Test if redirect happend more than special value
    worker              spawn a worker and subscribe task queue
    testgen_pls         Testcase generator based on current server's behaviors
    run_pls             Run testcases
    wait_mq_ready       Check if mq server is ready

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbosity       verbos display
  --version             verion info
```

Same as before, first we have to have urllis. Let's get urllist from `geturlc` command here.
```
# __CMD__ geturlc -e https://www.uniqlo.com/ -o urllist.txt -D www.uniqlo.com

# ls
urllist.txt  <=== Generated!
```

Then, run `testgen` in parallel using `testgen_pls` command:
```
$ __CMD__ testgen_pls -i urllist.txt -o testcase.json -s www.uniqlo.com.edgekey.net -d e13663.x.akamaiedge-staging.net 

Connecting Mongo...
FractMan: waiting results ...0 / 189
FractMan: waiting results ...85 / 189
removing db tables


# ls
urllist.txt
testcase.json  <=== Generated!
```

Next, do `run` in parallel using `run_pls` command:
```
# __CMD__ run_pls -i testcase.json

Connecting Mongo...
FractMan: waiting results ...0 / 188
FractMan: waiting results ...21 / 188
FractMan: waiting results ...64 / 188
FractMan: waiting results ...114 / 188
FractMan: waiting results ...163 / 188

Summary
=================

Tests not passed
----------------

Total
----------------
ran 188 tests: 0 failed

=> OK


# ls
urllist.txt
testcase.json
frdiff20190616021244806694.yaml  <=== Generated!
fret20190616021244806694.json  <=== Generated!
frsummary20190616021244806694.txt  <=== Generated!
```

Following workflow, i.e. retry failed test and merge testcases, is totally same as before.



#### 3. shutdown and cleanup __NAME__ worker

Once all workflow completed, you can clean up __NAME__ worker enviroment.

```
(exit from __NAME__ container)
# exit

(shell on host machine)
$ docker-compose down
docker-compose down
Stopping test_worker_4   ... done
Stopping test_worker_1   ... done
Stopping test_worker_2   ... done
Stopping test_worker_3   ... done
Stopping test_fract_1    ... done
Stopping test_rabbitmq_1 ... done
Stopping test_mongodb_1  ... done
Removing test_fract_run_85116ef5a98e ... done
Removing test_worker_4               ... done
Removing test_worker_1               ... done
Removing test_worker_2               ... done
Removing test_worker_3               ... done
Removing test_fract_1                ... done
Removing test_rabbitmq_1             ... done
Removing test_mongodb_1              ... done
Removing network test_default
```


That's it!
