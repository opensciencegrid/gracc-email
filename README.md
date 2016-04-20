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