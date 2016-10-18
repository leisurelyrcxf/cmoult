#Cmoult

Cmoult is the C couterpart of Pymoult. It provides DSU mechanisms
ready to be combined for designing dynamic updates.

Cmoult relies on libuminaty, provided in this repository, to read
DWARF informations and modify running binaries.

###Acknowledgement

The work on Pymoult, Cmoult and other derivatives is funded by the Brittany Regional Council in the context of project IMAJD.


##LICENCE

Cmoult is published under the GPLv2 license (see LICENSE.txt)


##Building

you should set the path of the project first. e.g. export CMOULT_PROJECT_HOME=ur_cmoult_project_home

Make a _build directory in the current folder and run cmake from here

`mkdir _build && cd _build && cmake ..`


