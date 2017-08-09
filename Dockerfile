FROM opensciencegrid/osg-wn

RUN yum -y install gfal2 gfal2-python gfal2-plugin-gridftp

RUN python setup.py install

ADD . /gracc-email
WORKDIR /gracc-email
RUN python setup.py install

