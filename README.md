#Pymoult

Pymoult is a Pypy library providing a prototyping platform for dynamic
software updates (DSU). It provides as many DSU mechanisms from the
literature as possible through a generic API.

To read the manual of Pymoult, please follow [this link](http://bitbucket.org/smartinezgd/pymoult/wiki/Pymoult%20manual)

A simple tutorial to Pymoult is available [here](http://bitbucket.org/smartinezgd/pymoult/wiki/A%20simple%20Pymoult%20tutorial)

##Acknowledgement

The work on Pymoult, Cmoult and other derivatives is funded by the Brittany Regional Council in the context of project IMAJD.


##LICENSE

Pymoult is published under the GPLv2 license (see LICENSE.txt)

Pypy-Dsu (required by Pymoult) is a fork of Pypy, published under specific licenses.

##Installing

Pymoult requires CPython-dsu, a Python interpreter enhanced with DSU
features.

###Installing CPython-dsu

Pymoult requires CPython-dsu, our custom python interpreter providing DSU
utilities. You can download and compile the source code from [the download page](https://bitbucket.org/smartinezgd/pymoult/downloads)

###Installing on Linux

1. Install python-dsu by compiling the sources

2. Install pymoult

	$> python setup.py install --prefix=<your_prefix>

3. Export your new PYTHONPATH
	
	$> export PYTHONPATH=$PYTHONPATH:<your_prefix>/site-packages	 

##Pydoc

The pydoc can be generated with the doc.sh script

	$> bash doc.sh

The pydoc will be generated in the doc folder, open doc/pymoult.html to start
browsing.

##Virtual Machine

Virtaul Machines preconfigured with pypy-dsu and Pymoult.

[Debian VM for Pymoult v3](https://partage.mines-telecom.fr/public.php?service=files&t=29660336d08df1374ee9ade5d2afede9&download) (Remember to update the installation of Pymoult before using it)

[Archlinux VM for Pymoult v2](https://partage.mines-telecom.fr/public.php?service=files&t=0ba628d67cf115064c39914f0b57dd08&download)

##Older version : using Pypy-dsu

The older version of pymoult uses Pypy-dsu. Although it is no longer
maintained, it is possible to download and use it.

###Installing Pypy-dsu

Pymoult requires Pypy-Dsu, our custom pypy interpreter providing DSU
utilities. You can download and compile the source code or install the
binaries from [the download page](https://bitbucket.org/smartinezgd/pymoult/downloads)

ArchLinux or Debian users may use the pre-compiled packages from the
[the download page](https://bitbucket.org/smartinezgd/pymoult/downloads).

To use the latest version of Pymoult, you need to install pypy-dsu-2.4-2.

###Installing on Linux

1. Install pypy-dsu your favorite way

2. Clone the pymoult repository

3. Update your local copy to the pypy-dsu version

    $> hg update pypy-dsu

4. Install pymoult

	$> pypy-dsu setup.py install --prefix=<your_prefix>

5. Export your new PYTHONPATH
	
	$> export PYTHONPATH=$PYTHONPATH:<your_prefix>/site-packages	 




