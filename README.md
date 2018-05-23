fract
=============

A web tool for CDN regression test


Overview
-------------

tbd...

Installation
------------

### Docker Image

Faster and handy way to quickly start.

```
$ docker pull ktmrmshk/fract

$ docker run -it ktmrmshk/fract /bin/bash

root@3f10471d9422:/# fract -h
usage: fract [-h] [-v] {geturlc,testgen,run,tmerge,rmerge,j2y,y2j} ...

positional arguments:
  {geturlc,testgen,run,tmerge,rmerge,j2y,y2j}
                        sub-command help

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbosity       verbos display

```

Workflow Example - Usage
------------

### 1. Collect URL list

Testcase is generated based on specific URL, so that you need to collect URLs and put it together single text file.
Fract helps collect URLs using built-in crawler.

```
$ fract geturlc -e https://www.abc123.com/ -d 1 -o urllist.txt -D www.abc123.com
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


### 2. Make testcases from URL list

Next step is making testcase from URL list. To this end, you need to know the hostname or IP address of both

* webserver/ghost that you refer as a original/base bahavior - refered as "source ghost"
* webseever/ghost that you try to test - refered as "destination/taret ghost"

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

In this case, source server is `www.abc123.com.edgekey.net`, while dest server is 'e1234.b.akamaiedge-staging.net'.
With that, testgeases can be generated as follows.

```
$ fract -v testgen -i urllist.txt -o testcase.json -s www.abc123.com.edgekey.net -d e1234.b.akamaiedge-staging.net

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



### 7. merge testcases

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


### 8. Next round

Go to #1, #2 or #3.

























