GRACC Collector Email Report
============================

The GRACC email reports generate readable status notifications of the GRACC collector.


Installation
------------

Install required packages in a virtualenv:
```
$ virtuanenv gracc-venv
$ . gracc-venv/bin/activate
$ pip install -r requirements.txt
```

Running GRACC-Email
-------------------

Run the `report.py` script with the emails as the command line arguments:
```
$ src/report.py <email> <email>
```

The output from running will arrive in email.  It will appear as:
```
Total records:
+-------------+---------+---------+
|   Yesterday |   Today | Delta   |
+=============+=========+=========+
|      972818 | 1104047 | -11.89% |
+-------------+---------+---------+
---------------------------------------------------------------------------
Records by Probe:
+--------------------------------------------------+---------------------+-----------------+-------------+
| ProbeName                                        |   Yesterday Records |   Today Records | Delta       |
+==================================================+=====================+=================+=============+
| condor:sub-1.icecube.wisc.edu                    |               11128 |            5970 | -46.35%     |
+--------------------------------------------------+---------------------+-----------------+-------------+
| pbs:carter-osg.rcac.purdue.edu                   |                 540 |             339 | -37.22%     |
+--------------------------------------------------+---------------------+-----------------+-------------+
| gridftp-transfer:top.ucr.edu                     |                 120 |             112 | -6.67%      |
+--------------------------------------------------+---------------------+-----------------+-------------+
| lsf:osgserv01.slac.stanford.edu                  |               16961 |           16542 | -2.47%      |
+--------------------------------------------------+---------------------+-----------------+-------------+
| gridftp-transfer:gluskap.phys.uconn.edu          |                 279 |             554 | +98.57%     |
+--------------------------------------------------+---------------------+-----------------+-------------+
| pbs:cms.rc.ufl.edu                               |                  18 |               0 | -100.00%    |
+--------------------------------------------------+---------------------+-----------------+-------------+
| condor:cit-gatekeeper2.ultralight.org            |                 672 |             433 | -35.57%     |

...
```


GRACC Backup Report
-------------------

The GRACC backup report can be run within Docker.  It needs a hostcert.pem and hostkey.pem in order to make the proxy and communicate with the remote servers.  A valid command would be:

    sudo docker run --rm -i -t --net=host -v /etc/grid-security/hostcert.pem:/hostcert.pem -v /etc/grid-security/hostkey.pem:/hostkey.pem run_backup_report


License
-------
Copyright 2016 Derek Weitzel

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
