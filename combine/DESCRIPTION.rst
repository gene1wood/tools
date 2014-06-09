How to Build
============
The RPM dependencies have to be created explicity (instead of being derived 
from the setup.py requirements) because PyYAML is called "PyYAML" in PyPi
and "PyYAML" in EPEL instead of "python-PyYAML"

::

    sudo yum install http://ftp.linux.ncsu.edu/pub/epel/6/i386/epel-release-6-8.noarch.rpm
    sudo yum install rubygems ruby-devel gcc python-setuptools rpm-build
    sudo easy_install pip
    sudo gem install fpm
    git clone https://github.com/gene1wood/tools.git
    
    cd tools/combine # This is required
    fpm -s python -t rpm --workdir ../ --no-python-dependencies --depends python-argparse --depends PyYAML ./setup.py
