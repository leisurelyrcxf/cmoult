#Pymoult

Pymoult is a Pypy library providing a prototyping platform for dynamic
software updates (DSU). It provides as many DSU mechanisms from the
literature as possible through a generic API.

To read the manual of Pymoult, please follow [this link](http://bitbucket.org/smartinezgd/pymoult/wiki/Pymoult%20manual)


##LICENSE


Pymoult is published under the GPLv2 license (see LICENSE.txt)

Pypy-Dsu (required by Pymoult) is a fork of Pypy, published under specific licenses.

##Installing


###Installing Pypy-dsu

Pymoult requires Pypy-Dsu, our custom pypy interpreter providing DSU
utilities. You can download and compile the source code or install the
binaries from [the download page](https://bitbucket.org/smartinezgd/pymoult/downloads)

ArchLinux users may use the
[package from AUR](https://aur.archlinux.org/packages/pypy-dsu/) or
the pre-compiled packages from the
[the download page](https://bitbucket.org/smartinezgd/pymoult/downloads).

To use the latest version of Pymoult, you need to install pypy-dsu-2.4-2.


###Installing on Linux

1. Install pypy-dsu your favorit way

2. Install pymoult

	$> pypy-dsu setup.py install --prefix=<your_prefix>

3. Export your new PYTHONPATH
	
	$> export PYTHONPATH=$PYTHONPATH:<your_prefix>/site-packages	 


###Installing on Archlinux

You can install pymoult using the AUR package [pypy-pymoult-hg](https://aur.archlinux.org/packages/pypy-pymoult-hg/)


##Pydoc


The pydoc can be generated with the doc.sh script

	$> bash doc.sh

The pydoc will be generated in the doc folder, open doc/pymoult.html to start
browsing.

##Virtual Machine

Virtaul Machines preconfigured with pypy-dsu and Pymoult.

[Debian VM for Pymoult v3](https://partage.mines-telecom.fr/public.php?service=files&t=29660336d08df1374ee9ade5d2afede9&download) (Remember to update the installation of Pymoult before using it)

[Archlinux VM for Pymoult v2](https://partage.mines-telecom.fr/public.php?service=files&t=0ba628d67cf115064c39914f0b57dd08&download)

