GRACC Collector Email Report
============================

The GRACC email reports generate readable status notifications of the GRACC backup.


GRACC Backup Report
-------------------

The GRACC backup report can be run within Docker.  It needs a hostcert.pem and hostkey.pem in order to make the proxy and communicate with the remote servers.  A valid command would be:

    sudo docker run --rm -i -t --net=host -v /etc/grid-security/hostcert.pem:/hostcert.pem -v /etc/grid-security/hostkey.pem:/hostkey.pem run_backup_report <email>


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
