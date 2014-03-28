#!/bin/bash

pydoc=`whereis pydoc | cut -d' ' -f3`

if [[ -d doc ]]
then
	rm -rf doc
fi
	mkdir doc
	pypy $pydoc -w ./
	rm setup.html
	mv *.html doc
	rm -f pymoult/*/*.pyc
	rm -f pymoult/*.pyc
	rm -f *.pyc
