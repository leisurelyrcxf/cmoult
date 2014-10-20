#Pymoult

Pymoult is a Pypy library providing a prototyping platform for dynamic
software updates (DSU). It provides as many DSU mechanisms from the
literature as possible through a generic API.

To read more about dynamic software updates and how Pymoult
contributes to this domain you can read the [wiki page on DSU](http://bitbucket.org/smartinezgd/pymoult/wiki/Dynamic%20Software%20Updates)

To read the manual of Pymoult, please follow [this link](http://bitbucket.org/smartinezgd/pymoult/wiki/Pymoult%20manual)


LICENSE
=======

Pymoult is published under the GPLv2 license (see LICENSE.txt)

Pypy-Dsu (required by Pymoult) is a fork of Pypy, published under specific licenses.

Installing
==========


Requirements
------------

Pymoult requires Pypy-Dsu, our custom pypy interpreter enhanced with specific DSU functionalists. You can install it by following the instructions [here](http://bitbucket.org/smartinezgd/pymoult/wiki/pypy-dsu)

Installing on Linux
-------------------

1. Install the _distribute_ module for pypy your favorite way

2. Install pymoult

	$> pypy setup.py install --prefix=<your_prefix>

3. Export your new PYTHONPATH
	
	$> export PYTHONPATH=$PYTHONPATH:<your_prefix>/site-packages	 


Installing on Archlinux
-----------------------

A package is available on AUR here :

http://aur.archlinux.org/packages/pypy-pymoult-hg


Pydoc
=====

The pydoc can be generated with the doc.sh script

	$> bash doc.sh

The pydoc will be generated in the doc folder, open doc/pymoult.html to start
browsing.

Virtual Machine
===============

A Virtual machine with the custom pypy-dsu installed as well as Pymoult can be downloaded on the following link.


[VM download link](https://partage.mines-telecom.fr/public.php?service=files&t=b9ae9bdffe6f9d1c6be2b8e100543ff5&download)
