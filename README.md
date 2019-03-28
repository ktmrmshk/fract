fract
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
$ docker pull ktmrmshk/fract

$ docker run -it ktmrmshk/fract /bin/bash

root@3f10471d9422:/# fract -h
Version: v0.6-3-g46db14d
usage: fract [-h] [-v] [--version]
             {geturlc,geturlakm,testgen,run,tmerge,rmerge,j2y,y2j,redirsum,ercost}
             ...

positional arguments:
  {geturlc,geturlakm,testgen,run,tmerge,rmerge,j2y,y2j,redirsum,ercost}
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


Workflow Example - Usage
------------

### 1. Collect URL list

#### A. Using crawler

Testcase is generated based on specific URL, so that you need to collect URLs and put it together single text file.
Fract helps collect URLs using built-in crawler.

```
$ fract geturlc -e https://www.abc123.com/ -d 1 -o urllist.txt -D www.abc123.com
```

Show help to get more details:

```
$ fract geturlc -h

usage: fract geturlc [-h] -e ENTRYPOINT [-d DEPTH] -o OUTPUT -D DOMAIN
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
$ fract geturlakm -i top_u_r_l_hits_1.csv top_u_r_l_hits_2.csv -D www.abc123.com -p https -o urllist.txt
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
$ fract -v testgen -i urllist.txt -o testcase.json -s www.abc123.com.edgekey.net -d e1234.b.akamaiedge-staging.net
```


If you like to modify or append custom request header like User-Agent and Referer, use `-H` option with json-formatted custom headers and values.


```
$ fract -v testgen -H '{"User-Agent": "iPhone", "Referer": "http://www.abc.com/"}' -i urllist.txt -o testcase.json -s www.abc123.com.edgekey.net -d e1234.b.akamaiedge-staging.net 

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
$ fract -v run -i testcase.json

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
$ fract y2j frdiff20180523141553196655.yaml frdiff20180523141553196655.json
```

Then, it's time to re-run.

```
$ fract -v run -i frdiff20180523141553196655.json
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
$ fract rmerge -t testcase.json frdiff*.json -r fret* -s final_summary.txt -o final_result.json

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
$ fract tmerge -t testcase.json frdiff*.json -o final_testcase.json 

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
$ fract redirsum -t final_testcase.json -r final_result.json -o redirect_summary.json

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
$ fract ercost -c 1000000 -t final_testcase.json -r final_result.json -o ercost_summary.json.test

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

























