export ELFUTILS_INCLUDES = /usr/include/elfutils
export ELFUTILS_LIBS = /usr/lib/x86_64-linux-gnu
export CFLAGS = -Wall -Wextra -std=c99 -I$(ELFUTILS_INCLUDES)

all: static dynamic testmanager prog

lib: static dynamic

prog: dummy
	cd testprogs/src; $(MAKE) $(MFLAGS)
	mkdir -p bin
	cp -uf testprogs/bin/* bin/

testmanager: dummy
	cd testmanager/src; $(MAKE) $(MFLAGS)
	mkdir -p bin
	cp -uf testmanager/bin/* bin/

dynamic: dummy
	cd lib/src; ./configure dynamic && $(MAKE) cleanlight && $(MAKE) $(MFLAGS) dynamic
	mkdir -p bin
	cp -uf lib/bin/* bin/

static: dummy
	cd lib/src; ./configure static && $(MAKE) cleanlight && $(MAKE) $(MFLAGS) static
	mkdir -p bin
	cp -uf lib/bin/* bin/
	mkdir -p include
	cp -uf lib/include/libuminati.h include

dummy:
	true

clean:
	cd lib/src; $(MAKE) $(MFLAGS) $@
	cd testmanager/src; $(MAKE) $(MFLAGS) $@
	cd testprogs/src; $(MAKE) $(MFLAGS) $@

cleanall: 
	cd lib/src; $(MAKE) $(MFLAGS) $@
	cd testmanager/src; $(MAKE) $(MFLAGS) $@
	cd testprogs/src; $(MAKE) $(MFLAGS) $@
	rm -rf bin
	rm -rf include
