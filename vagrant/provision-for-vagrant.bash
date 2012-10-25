#!/bin/bash -x

rpm -q redhat-release oracle-release centos-release sl-release &>/dev/null; if [ $? -ge 4 ]; then echo "This is not a Redhat based system. Aborting"; exit 1; fi

# vagrant user
groupadd admin
useradd -G admin vagrant
usermod -p $(echo "vagrant" | openssl passwd -1 -stdin) vagrant
id vagrant

# sudoers
echo "%admin ALL=NOPASSWD: ALL" >> /etc/sudoers
echo "Defaults    env_keep+=SSH_AUTH_SOCK" >> /etc/sudoers
sed -i -e 's/^\(Defaults[ \t]*requiretty\)/#\1/g' /etc/sudoers
echo "/etc/sudoers" && cat /etc/sudoers

# Virtualbox Guest Additions
# http://wiki.centos.org/HowTos/Virtualization/VirtualBox/CentOSguest
# Enable EPEL
rpm -ivh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-7.noarch.rpm
buildtools="gcc make perl kernel-devel-`uname -r`"
yum install -y dkms $buildtools
mkdir /media/cdrom
mount /dev/cdrom /media/cdrom
/media/cdrom/VBoxLinuxAdditions.run
echo "Getting \"Installing the Window System drives  [FAILED]\" is ok"
echo "This is because we have no GUI installed"
yum remove -y $buildtools

# hostname and domain
newhostname="vagrant-`/usr/lib/dkms/lsb_release -is`-`/usr/lib/dkms/lsb_release -rs`"
sed -i -e "s/^127\.0\.0\.1\([ \t]*\)local/127.0.0.1\1$newhostname local/g" -e "s/^::1\([ \t]*\)local/::1\1$newhostname local/g" /etc/hosts
sed -i -e "s/^HOSTNAME=.*/HOSTNAME=$newhostname/g" -e "s/^DOMAIN=.*/DOMAIN=vagrantup.com/g" /etc/sysconfig/network
echo "/etc/hosts" && cat /etc/hosts
echo "/etc/sysconfig/network" && cat /etc/sysconfig/network

# Vagrant requirements
yum install -y openssh-clients wget
wget -O /tmp/vagrant.pub /tmp/ https://raw.github.com/mitchellh/vagrant/master/keys/vagrant.pub
install -d -g vagrant -o vagrant -m 0700 /home/vagrant/.ssh
install -D -g vagrant -o vagrant -m 0600 /tmp/vagrant.pub /home/vagrant/.ssh/authorized_keys
rm /tmp/vagrant.pub
ls -al /home/vagrant/.ssh

# Disable ssh dns lookups
if grep "^UseDNS[ \t]*yes" /etc/ssh/sshd_config; then sed -i -e 's/^\(UseDNS[ \t]*\)yes/\1no/g' /etc/ssh/sshd_config; else echo "UseDNS no" >> /etc/ssh/sshd_config
echo "/etc/ssh/sshd_config" && cat /etc/ssh/sshd_config

# speedup boot
sed -i -e 's/timeout=.*/timeout=1/g' /boot/grub/menu.lst
echo "/boot/grub/menu.lst" && cat /boot/grub/menu.lst

# chef
curl -L https://www.opscode.com/chef/install.sh | bash
chef-client -v
