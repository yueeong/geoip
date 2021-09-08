# IP Lookup Utility
A Python CLI tool to analyze apache log files in combined format.

It will output two formatted reports consisting of 3 columns each, listing the top ten largest source of visits by Country and by US State.

Apart from inline, HTML snippet can be output for use in a webpage.

The utility gets IP location data from Maxmind's [GeoLite2 City database](http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz)
and leverages their Python module [geoip2](https://pypi.python.org/pypi/geoip2)


Output sample :
```bash
+----------------+----------+------------------------+
| Country        |   Visits | Most Visited Page      |
|----------------+----------+------------------------|
| United States  |    14092 | /site/clone_entry_form |
| Netherlands    |     3205 | /site/clone_entry_form |
| China          |     1466 | /user/login_form       |
| Germany        |     1233 | /entry/20252           |
| France         |      685 | /site/clone_entry_form |
| United Kingdom |      297 | /site/search           |
| Canada         |      206 | /region/60/filter      |
| Mexico         |      119 | /region/2728/filter    |
| Japan          |       64 | /region/364            |
| Israel         |       54 | /entry/20254           |
+----------------+----------+------------------------+
```



Apache format config :
```
LogFormat "%h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"" combined

```

### Usage
From linux command line: _(Add -v for more verbose logging. Disabled by default)_
If the input apache access.log file is large, please be patient while it processes.

```bash
(myvirtualenv) root@myhost:~/yueeong-geoiphw-d19eb41953f5# python visitor_reporter.py -f access.log
```

```bash
usage: visitor_reporter.py [-h] -f LOG_FILE_PATH [-db MMDB_FILE_PATH]
                           [-r REPORT_STYLE] [-v]

Geo IP reporting tool.

optional arguments:
  -h, --help            show this help message and exit
  -f LOG_FILE_PATH, --file LOG_FILE_PATH
                        Enter path to apache log file to parse. Mandatory.
  -db MMDB_FILE_PATH, --dbfile MMDB_FILE_PATH
                        Enter alternative path MaxMind db file. Default
                        ./data/GeoLite2-City.mmdb
  -r REPORT_STYLE, --report_style REPORT_STYLE
                        Style of output report. Valid types : plain, psql,
                        html, grid, rst
  -v, --quiet           Bool. Set to quiet logs in terminal

```

_Note: there is warning output from a Pandas Dataframe function during execution. It is safe to ignore for now._


### Installation

Running from a Python virtualenv will give the cleanest experience.

#### on Ubuntu 16.04
Ensure Python 3 and Git are installed.

On Ubuntu 16.04, the installed version is 3.5.2

Ensure python virtualenv is installed, as root:
```bash
apt-get install git
apt-get install python3-venv
```
In your desired directory, create the python virtual environment, cd into and activate it:

(Note: _`you do not have to run as root. Once the apt-get system installs are completed, you can proceed as a normal user.`_)
```bash
root@myhost:~# pyvenv-3.5 myvirtualenv
root@myhost:~# cd myvirtualenv/
root@myhost:~/myvirtualenv# source bin/activate
(myvirtualenv) root@myhost:~/myvirtualenv#

```

Download the latest repo version here : https://bitbucket.org/yueeong/geoiphw/get/master.tar.gz
and un-tar in the directory of your choosing
```bash
(myvirtualenv) root@myhost:~# wget https://bitbucket.org/yueeong/geoiphw/get/master.tar.gz
(myvirtualenv) root@myhost:~# tar zxvf master.tar.gz 
(myvirtualenv) root@myhost:~# cd yueeong-geoiphw-<commit_number>/

```

Install the necessary pre-requisite python modules with the included requirements.txt file like so :
```bash
(myvirtualenv) root@myhost:~/yueeong-geoiphw-<commit_number># pip install -r requirements.txt

```
Get the IP location reference database 
```bash
(myvirtualenv) root@myhost:~/yueeong-geoiphw-<commit_number># cd data
(myvirtualenv) root@myhost:~/yueeong-geoiphw-<commit_number>/data# wget http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz
(myvirtualenv) root@myhost:~/yueeong-geoiphw-<commit_number>/data# gunzip GeoLite2-City.mmdb.gz 
```

You are now ready to run the reporter. 
Execute as described in the Usage section.



#### To Do
- [] input data cleaning. Reverse DNS lookup on apache log files with hostnames instead of ip
- [] enhance error checking for db files, user input, apache file formatting etc
- [] enhance logging messages

