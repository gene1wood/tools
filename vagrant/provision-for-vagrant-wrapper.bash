#!/bin/bash
# To install run curl -L http://bit.ly/TZLYrX | bash
#
curl -L https://raw.github.com/gene1wood/tools/master/vagrant/provision-for-vagrant.bash | bash 2>&1 | tee -a /tmp/provision-for-vagrant.log
echo "Read the provisioning log here : /tmp/provision-for-vagrant.log"

