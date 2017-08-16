#!/bin/sh

# Create a proxy for gfal, because it segfaults with the normal certs
grid-proxy-init -cert /etc/grid-security/gracc.opensciencegrid.org-cert.pem -key /etc/grid-security/gracc.opensciencegrid.org-key.pem -out /etc/grid-security/gracc.opensciencegrid.org-proxy.pem


# Run the actual command
docker run --rm --net=host -v /etc/grid-security/gracc.opensciencegrid.org-proxy.pem:/tmp/x509up_u0 -v /home/dweitzel/test.toml:/test.toml djw8605/gracc-email:add_backup_report backup_report -c /test.toml djw8605@gmail.com

