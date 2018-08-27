FROM opensciencegrid/osg-wn:3.4-el6

RUN pip install --upgrade setuptools

ADD test.toml /test.toml

ADD . /gracc-email
WORKDIR /gracc-email
RUN python setup.py install


