FROM opensciencegrid/osg-wn

ADD . /gracc-email
WORKDIR /gracc-email
RUN python setup.py install

