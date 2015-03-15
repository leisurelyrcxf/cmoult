export ELFUTILS_INCLUDES = /usr/include/elfutils
export ELFUTILS_LIBS = /usr/lib/x86_64-linux-gnu
export CFLAGS = -Wall -Wextra -std=c99 -I$(ELFUTILS_INCLUDES)

SRCARNAUD = ../libuminati
TESTCFLAGS = $(CFLAGS) -I$(SRCARNAUD)/lib/include
TESTLDFLAGS = -L$(SRCARNAUD)/bin -L$(ELFUTILS_LIBS) -luminati -ldw -lelf

all: libama

manager: manager.o
	gcc -o manager manager.o $(TESTLDFLAGS)

manager2: manager2.o
	gcc -o manager2 manager2.o $(TESTLDFLAGS)

libama: 
	gcc -g -O0 -c libama.c $(TESTLDFLAGS) $(TESTCFLAGS)
	gcc -o libtest libtest.c libama.o $(TESTLDFLAGS) $(TESTCFLAGS)
	gcc -o lamanager lamanager.c libama.o $(TESTLDFLAGS) $(TESTCFLAGS)
	gcc -o lamanager2 lamanager2.c libama.o $(TESTLDFLAGS) $(TESTCFLAGS)

.c.o:
	gcc -c $(TESTCFLAGS) $<

dummy:
	true

clean:
	rm -f *.o

cleanall: 
	rm -f *.o
