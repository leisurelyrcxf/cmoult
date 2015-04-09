TESTCFLAGS = $(CFLAGS) -I../include -I../../lib/include
TESTLDFLAGS = -L../../bin -L$(ELFUTILS_LIBS) -luminati -ldw
TESTFILES = debug.o track.o

testmanager: $(TESTFILES)
	gcc -o track $(TESTFILES) $(TESTLDFLAGS)
	mkdir -p ../bin
	mv -f track ../bin

.c.o:
	gcc -c $(TESTCFLAGS) $<

clean:
	rm -f *.o

cleanall: 
	rm -f *.o
	rm -rf ../bin
