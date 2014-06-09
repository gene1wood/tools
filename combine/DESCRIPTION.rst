How to Build
============

::

    sudo yum install http://ftp.linux.ncsu.edu/pub/epel/6/i386/epel-release-6-8.noarch.rpm
    sudo yum install rubygems ruby-devel gcc python-setuptools rpm-build
    sudo easy_install pip
    sudo gem install fpm
    git clone https://github.com/gene1wood/tools.git
    
    cd tools/combine # This is required
    fpm -s python -t rpm --workdir ../ --debug ./setup.py
