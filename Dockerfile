FROM opensciencegrid/osg-wn

RUN yum -y install python-setuptools

ADD . /gracc-email
WORKDIR /gracc-email
RUN python setup.py install

