#!/bin/bash

base=$(basename $1 .c)


gcc -std=c11 -fPIC -c "$1"

gcc -std=c11 -shared -Wl,-soname,"$base".so.1 -o "$base".so "$base".o
