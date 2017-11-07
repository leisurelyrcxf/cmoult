#Libuminati

Libumaniti is a C library providing tools for introspection and dynamic modification of running C programs. It requires libdw for reading DWARF informations.

###Acknowledgement

The work on Pymoult, Cmoult and other derivatives is funded by the Brittany Regional Council in the context of project IMAJD.


##LICENCE

Libuminati is published under the GPLv2 license (see LICENSE.txt)






Compilation : ./configure (pour récupérer le chemin de libdw) make

Les exécutables et la lib sont dans bin, le .h est dans include
Penser à mettre LD_LIBRARY_PATH si nécessaire
