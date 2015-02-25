export ELFUTILS_INCLUDES = /usr/include/elfutils
export ELFUTILS_LIBS = /usr/lib/x86_64-linux-gnu
export CFLAGS = -Wall -Wextra -std=c99 -I$(ELFUTILS_INCLUDES)

SRCARNAUD = ../../libuminati
TESTCFLAGS = $(CFLAGS) -I$(SRCARNAUD)/lib/include
TESTLDFLAGS = -L$(SRCARNAUD)/bin -L$(ELFUTILS_LIBS) -luminati -ldw -lelf

all: demo1 managers

demo1: demo1.o
	gcc -o demo1 demo1.o $(TESTLDFLAGS) -static

managers: 
	gcc -o manager1 manager1.c ../../libama/libama.o $(TESTLDFLAGS) $(TESTCFLAGS)
	gcc -o manager2 manager2.c ../../libama/libama.o $(TESTLDFLAGS) $(TESTCFLAGS)
	gcc -o manager3 manager3.c ../../libama/libama.o $(TESTLDFLAGS) $(TESTCFLAGS)

.c.o:
	gcc -c $(TESTCFLAGS) -g $<

dummy:
	true

clean:
	rm -f *.o

cleanall: 
	rm -f *.o
