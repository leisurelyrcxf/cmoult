PROGCFLAGS = -g
PROGLDFLAGS = -static
PROGFILES = prog

all: testprogs update

testprogs: $(PROGFILES)

update: update.c
	gcc -fPIC -c $(PROGCFLAGS) update.c
	gcc -shared -o update.so update.o
	mkdir -p ../bin
	mv -f update.so ../bin

prog: prog.o
	gcc $(PROGLDFLAGS) -o prog prog.o
	mkdir -p ../bin
	mv -f prog ../bin

.c.o:
	gcc -c $(PROGCFLAGS) $<

clean:
	rm -f *.o

cleanall: 
	rm -f *.o
	rm -rf ../bin
