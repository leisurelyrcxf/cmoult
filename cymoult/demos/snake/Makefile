export ELFUTILS_INCLUDES = /usr/include/elfutils
export ELFUTILS_LIBS = /usr/lib/x86_64-linux-gnu
export CFLAGS = -Wall -Wextra -std=c99 -I$(ELFUTILS_INCLUDES)

SRCARNAUD = ../../libuminati
TESTCFLAGS = $(CFLAGS) -I$(SRCARNAUD)/lib/include
TESTLDFLAGS = -L$(SRCARNAUD)/bin -L$(ELFUTILS_LIBS) -luminati -ldw -lelf
SNAKEFLAGS = -lSDL -lSDL_image


all: snake managers

snake: snake.o
	gcc -o snake snake.o $(SNAKEFLAGS) -rdynamic

managers: 
	gcc -o manager manager.c ../../libama/libama.o $(TESTLDFLAGS) $(TESTCFLAGS)
	gcc -o manager2 manager2.c ../../libama/libama.o $(TESTLDFLAGS) $(TESTCFLAGS)

.c.o:
	gcc -c $(TESTCFLAGS) -g $<

dummy:
	true

clean:
	rm -f *.o

cleanall: 
	rm -f *.o
