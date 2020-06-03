FROM opensciencegrid/osg-wn:3.5

RUN yum -y install python-pip python-setuptools &&  pip install --upgrade setuptools pip

ADD test.toml /test.toml

ADD . /gracc-email
WORKDIR /gracc-email
RUN python setup.py install


