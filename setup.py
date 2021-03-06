#!/usr/bin/env pypy


if __name__ == "__main__":

	from distutils.core import setup

	setup(name="pymoult",
			version="0.1",
			description="Pypy DSU profiling library",
			author="Sebastien Martinez",
			author_email="sebastien.martinez@telecom-bretagne.eu",
			url="http://bitbucket.org/smartinezgd/pymoult",
			packages=["pymoult","pymoult.highlevel","pymoult.lowlevel"],
			license="GPLv2"
			)
